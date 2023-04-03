// Script that analyzes ASMedia ASM236x firmware.
// @author cyrozap
// @category ASMedia.ASM236x

// SPDX-License-Identifier: GPL-3.0-or-later

// Copyright (C) 2023  Forest Crossman <cyrozap@gmail.com>
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <https://www.gnu.org/licenses/>.

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.data.DataType;
import ghidra.program.model.data.DataTypeManager;
import ghidra.program.model.data.DataTypePath;
import ghidra.program.model.lang.Register;
import ghidra.program.model.listing.Data;
import ghidra.program.model.listing.Instruction;
import ghidra.program.model.listing.Listing;
import ghidra.program.model.listing.Program;
import ghidra.program.model.scalar.Scalar;
import ghidra.program.model.symbol.Reference;
import ghidra.program.model.symbol.ReferenceManager;
import ghidra.program.model.symbol.RefType;
import ghidra.program.model.symbol.SourceType;
import ghidra.program.model.symbol.Symbol;
import ghidra.program.model.util.CodeUnitInsertionException;
import ghidra.util.bytesearch.GenericMatchAction;
import ghidra.util.bytesearch.GenericByteSequencePattern;
import ghidra.util.bytesearch.Match;
import ghidra.util.bytesearch.MemoryBytePatternSearcher;
import ghidra.util.bytesearch.Pattern;
import ghidra.util.exception.CancelledException;
import ghidra.util.task.TaskDialog;

public class Asm236xFirmwareHelper extends GhidraScript {
	private Register DPTR;
	private Register DPL;
	private Register DPH;
	private Register R1;
	private Register R2;
	private Register R3;
	private Register R4;
	private Register R5;
	private Register R6;
	private Register R7;
	private Address DPL_addr;
	private Address DPH_addr;

	private Address createDataXrefsForU32WriteFunction(Instruction startInstruction) {
		Instruction prevInst = startInstruction.getPrevious();

		String mnemonic = prevInst.getMnemonicString();
		if (!mnemonic.equals("MOV")) {
			return null;
		}

		Object[] resultObjects = prevInst.getResultObjects();
		if (resultObjects.length < 1) {
			return null;
		}

		Object[] inputObjects = prevInst.getInputObjects();
		if (inputObjects.length < 1) {
			return null;
		}

		Object dst = resultObjects[0];
		Object src = inputObjects[0];
		if (!(dst instanceof Register && src instanceof Scalar)) {
			return null;
		}

		Register reg = (Register)dst;
		Scalar value = (Scalar)src;

		//printf("Register %s: 0x%04x\n", reg, value.getUnsignedValue());

		if (reg != DPTR) {
			return null;
		}

		long xdataRefAddrInt = value.getUnsignedValue() & 0xffff;
		Address xdataRefAddr = toAddr(String.format("EXTMEM:%04x", xdataRefAddrInt));
		ReferenceManager refManager = currentProgram.getReferenceManager();

		Address movAddress = prevInst.getAddress();
		refManager.removeAllReferencesFrom(movAddress);
		refManager.addMemoryReference(movAddress, xdataRefAddr, RefType.DATA, SourceType.USER_DEFINED, 1);
		printf(getScriptName() + "> Added reference from %s to %s.\n", movAddress, xdataRefAddr);

		Address startAddress = startInstruction.getAddress();
		refManager.addMemoryReference(startAddress, xdataRefAddr, RefType.WRITE, SourceType.USER_DEFINED, 1);
		printf(getScriptName() + "> Added reference from %s to %s.\n", startAddress, xdataRefAddr);

		return xdataRefAddr;
	}

	private Address findAddressByBytesMaskAndOffset(byte[] bytes, byte[] mask, int offset) throws CancelledException {
		List<Address> results = new ArrayList<Address>();
		GenericMatchAction<Address> action = new GenericMatchAction<Address>(null) {
			@Override
			public void apply(Program prog, Address addr, Match match) {
				results.add(addr);
			}
		};
		GenericByteSequencePattern pattern = new GenericByteSequencePattern(bytes, mask, action);
		MemoryBytePatternSearcher searcher = new MemoryBytePatternSearcher("findAddressByBytesMaskAndOffset",
				new ArrayList<Pattern>(Arrays.asList(pattern)));
		searcher.setSearchExecutableOnly(true);
		searcher.search(currentProgram, currentProgram.getMemory(), new TaskDialog("findAddressByBytesMaskAndOffset", true, false, true));

		if (results.size() < 1) {
			return null;
		}

		return results.get(0).add(offset);
	}

	private Address findCopyDwordLiteralFunction() throws CancelledException {
		// Get the function address.
		Address functionAddr = findAddressByBytesMaskAndOffset(
			new byte[] { (byte)0xa8, (byte)0x82,
					(byte)0x85, (byte)0x83, (byte)0xf0,
					(byte)0xd0, (byte)0x83,
					(byte)0xd0, (byte)0x82,
					(byte)0x12, (byte)0x00, (byte)0x00,
					(byte)0x12, (byte)0x00, (byte)0x00,
					(byte)0x12, (byte)0x00, (byte)0x00,
					(byte)0x12, (byte)0x00, (byte)0x00,
					(byte)0xe4, (byte)0x73 },
			new byte[] { (byte)0xff, (byte)0xff,
					(byte)0xff, (byte)0xff, (byte)0xff,
					(byte)0xff, (byte)0xff,
					(byte)0xff, (byte)0xff,
					(byte)0xff, (byte)0x00, (byte)0x00,
					(byte)0xff, (byte)0x00, (byte)0x00,
					(byte)0xff, (byte)0x00, (byte)0x00,
					(byte)0xff, (byte)0x00, (byte)0x00,
					(byte)0xff, (byte)0xff },
			0);
		if (functionAddr == null) {
			printf(getScriptName() + "> Failed to find copy dword literal function!\n");
			return null;
		}

		printf(getScriptName() + "> Found copy dword literal function: %s\n", functionAddr);

		return functionAddr;
	}

	private Address findSwitchCaseFunction() throws CancelledException {
		// Get the function address.
		Address functionAddr = findAddressByBytesMaskAndOffset(
			new byte[] { (byte)0xd0, (byte)0x83,
					(byte)0xd0, (byte)0x82,
					(byte)0xf8,
					(byte)0xe4,
					(byte)0x93 },
			new byte[] { (byte)0xff, (byte)0xff,
					(byte)0xff, (byte)0xff,
					(byte)0xff,
					(byte)0xff,
					(byte)0xff },
			0);
		if (functionAddr == null) {
			printf(getScriptName() + "> Failed to find switch-case function!\n");
			return null;
		}

		printf(getScriptName() + "> Found switch-case function: %s\n", functionAddr);

		return functionAddr;
	}

	private Address findU32WriteFunction() throws CancelledException {
		// Get the function address.
		Address functionAddr = findAddressByBytesMaskAndOffset(
			new byte[] { (byte)0xec, (byte)0xf0, (byte)0xa3,
					(byte)0xed, (byte)0xf0, (byte)0xa3,
					(byte)0xee, (byte)0xf0, (byte)0xa3,
					(byte)0xef, (byte)0xf0, (byte)0x22 },
			new byte[] { (byte)0xff, (byte)0xff, (byte)0xff,
					(byte)0xff, (byte)0xff, (byte)0xff,
					(byte)0xff, (byte)0xff, (byte)0xff,
					(byte)0xff, (byte)0xff, (byte)0xff },
			0);
		if (functionAddr == null) {
			printf(getScriptName() + "> Failed to find U32 write function!\n");
			return null;
		}

		printf(getScriptName() + "> Found U32 write function: %s\n", functionAddr);

		return functionAddr;
	}

	private void addCrossReferencesForU32Writes(Address functionAddr) throws CancelledException, CodeUnitInsertionException {
		if (functionAddr == null) {
			return;
		}

		DataTypeManager dtm = currentProgram.getDataTypeManager();
		DataTypePath u32DataTypePath = new DataTypePath("/stdint.h", "uint32_t");
		DataType u32DataType = dtm.getDataType(u32DataTypePath);
		if (u32DataType == null) {
			printf(getScriptName() + "> Failed to find data type \"%s\".\n", u32DataTypePath);
			return;
		}
		Listing listing = currentProgram.getListing();

		int referencedCount = 0;
		int definedCount = 0;

		// Loop over all the locations where the function is called.
		Reference[] calls = getReferencesTo(functionAddr);
		for (Reference call : calls) {
			Address callSite = call.getFromAddress();
			Instruction inst = getInstructionAt(callSite);

			Address u32Addr = createDataXrefsForU32WriteFunction(inst);
			if (u32Addr == null) {
				continue;
			}

			referencedCount += 1;

			// This skips all the non-null, defined data whose type doesn't start with "undefined".
			Data u32Data = getDataAt(u32Addr);
			if ( (u32Data != null) && !u32Data.getDataType().getName().startsWith("undefined") ) {
				continue;
			}

			// This is necessary to avoid destroying defined arrays.
			//
			// Addresses in the middle of an array are not undefined, but there's no Data object there
			// (u32Data == null), so the previous check won't catch them. To skip over those addresses in
			// arrays without defined data, We'll use the "isUndefined()" function.
			//
			// "isUndefined()" means u32Data is null and the address is not in an array. Conversely,
			// "!isUndefined()" then means there's either a Data object at that address (u32Data != null)
			// or the address is in an array. "NOT Data AND (Data OR in an array)" can be expanded to
			// "(NOT Data AND Data) OR (NOT Data AND in an array)", which simplifies to
			// "NOT Data AND in an array", which is exactly what we want to filter out to avoid clobbering
			// anything.
			if ( (u32Data == null) && !listing.isUndefined(u32Addr, u32Addr.add(u32DataType.getLength()-1)) ) {
				continue;
			}

			listing.clearCodeUnits(u32Addr, u32Addr.add(u32DataType.getLength()-1), false);
			listing.createData(u32Addr, u32DataType);

			printf(getScriptName() + "> Defined uint32_t at %s.\n", u32Addr);

			definedCount += 1;
		}

		printf(getScriptName() + "> Created references %d times and defined data %d times.\n", referencedCount, definedCount);
	}

	private void copyDwordFunctionHelper() throws CancelledException, CodeUnitInsertionException {
		Address functionAddr = findCopyDwordLiteralFunction();
		if (functionAddr == null) {
			return;
		}

		DataTypeManager dtm = currentProgram.getDataTypeManager();
		DataTypePath u32DataTypePath = new DataTypePath("/stdint.h", "uint32_t");
		DataType u32DataType = dtm.getDataType(u32DataTypePath);
		if (u32DataType == null) {
			printf(getScriptName() + "> Failed to find data type \"%s\".\n", u32DataTypePath);
			return;
		}
		Listing listing = currentProgram.getListing();
		int definedCount = 0;
		int disassembled = 0;

		// Loop over all the locations where the function is called.
		Reference[] calls = getReferencesTo(functionAddr);
		for (Reference call : calls) {
			Address callSite = call.getFromAddress();

			Address u32Addr = callSite.add(3);
			Data u32Data = getDataAt(u32Addr);
			if ( ( (u32Data == null) || u32Data.getDataType().getName().startsWith("undefined") ) &&
					( (u32Data != null) || listing.isUndefined(u32Addr, u32Addr.add(u32DataType.getLength()-1)) ||
					  (listing.getCodeUnitAt(u32Addr) != null) ) ) {
				listing.clearCodeUnits(u32Addr, u32Addr.add(u32DataType.getLength()-1), false);
				listing.createData(u32Addr, u32DataType);

				printf(getScriptName() + "> Defined uint32_t at %s.\n", u32Addr);

				definedCount += 1;
			}

			Address codeAddr = u32Addr.add(u32DataType.getLength());
			if (listing.isUndefined(codeAddr, codeAddr)) {
				listing.clearCodeUnits(codeAddr, codeAddr.add(2), false);
				disassemble(codeAddr);

				printf(getScriptName() + "> Disassembled code at %s.\n", codeAddr);

				disassembled += 1;
			}
		}

		printf(getScriptName() + "> Defined data %d times and disassembled %d times.\n", definedCount, disassembled);
	}

	private void switchTableFunctionHelper() throws CancelledException, CodeUnitInsertionException {
		Address functionAddr = findSwitchCaseFunction();
		if (functionAddr == null) {
			return;
		}

		DataTypeManager dtm = currentProgram.getDataTypeManager();
		DataType pointerDataType = dtm.getDataType(new DataTypePath("/", "pointer"));
		if (pointerDataType == null) {
			printf(getScriptName() + "> Failed to find \"pointer\" data type.\n");
			return;
		}
		DataType byteDataType = dtm.getDataType(new DataTypePath("/", "byte"));
		if (byteDataType == null) {
			printf(getScriptName() + "> Failed to find \"byte\" data type.\n");
			return;
		}
		DataType ushortDataType = dtm.getDataType(new DataTypePath("/", "ushort"));
		if (ushortDataType == null) {
			printf(getScriptName() + "> Failed to find \"ushort\" data type.\n");
			return;
		}

		Listing listing = currentProgram.getListing();
		int definedCount = 0;

		// Loop over all the locations where the function is called.
		Reference[] calls = getReferencesTo(functionAddr);
		for (Reference call : calls) {
			Address callSite = call.getFromAddress();

			Address currentAddr = callSite.add(3);
			printf(getScriptName() + "> Parsing jump table: %s\n", currentAddr);
			while (true) {
				listing.clearCodeUnits(currentAddr, currentAddr.add(1), false);
				listing.createData(currentAddr, ushortDataType);
				if (((Scalar)listing.getDataAt(currentAddr).getValue()).getValue() == (long)0) {
					// This is the end of the table, so create the pointer to the default case.
					currentAddr = currentAddr.add(2);
					listing.clearCodeUnits(currentAddr, currentAddr.add(1), false);
					listing.createData(currentAddr, pointerDataType);
					break;
				}

				listing.clearCodeUnits(currentAddr, currentAddr.add(2), false);
				listing.createData(currentAddr, pointerDataType);
				currentAddr = currentAddr.add(2);
				listing.createData(currentAddr, byteDataType);
				currentAddr = currentAddr.add(1);
			}

			definedCount += 1;
		}

		printf(getScriptName() + "> Found %d jump tables.\n", definedCount);
	}

	public void run() throws Exception {
		// Get the registers we care about.
		DPTR = currentProgram.getRegister("DPTR");
		DPL = currentProgram.getRegister("DPL");
		DPH = currentProgram.getRegister("DPH");
		R1 = currentProgram.getRegister("R1");
		R2 = currentProgram.getRegister("R2");
		R3 = currentProgram.getRegister("R3");
		R4 = currentProgram.getRegister("R4");
		R5 = currentProgram.getRegister("R5");
		R6 = currentProgram.getRegister("R6");
		R7 = currentProgram.getRegister("R7");

		// Get the addresses of the SFRs.
		DPL_addr = toAddr("SFR:82");
		DPH_addr = toAddr("SFR:83");

		copyDwordFunctionHelper();
		//switchTableFunctionHelper();
		//addCrossReferencesForU32Writes(findCopyDwordLiteralFunction());
		//addCrossReferencesForU32Writes(findU32WriteFunction());
	}
}
