#!/usr/bin/env python3

import urllib.request
import json
import csv
import os, sys
import time
import os
import subprocess
import struct
import serial
import platform
import getopt, sys
import serial.tools.list_ports
import ntpath
import shutil
import webbrowser
import re
import zipfile
import wave
import hashlib
from ctypes import *
import enum
from dataclasses import dataclass

PROGRAM_NAME = "OpenGD77 Prompt Studio"
PROGRAM_VERSION = "0.3.1"


def is_frozen_app():
    return bool(getattr(sys, "frozen", False))


def application_base_dir():
    if is_frozen_app():
        return os.path.dirname(os.path.abspath(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))

FLASH_SEND_SIZE = 8
MAX_USB_TRANSFERT_SIZE = 1024
MAX_TRANSFER_SIZE = MAX_USB_TRANSFERT_SIZE - FLASH_SEND_SIZE
VOICE_PROMPTS_SIZE_MAX = 0x28C00 ## max available FLASH space
CREATE_NO_WINDOW = 0x08000000
DETACHED_PROCESS = 0x00000008
overwrite = False
gain = '0'
atempo = '1.5'
atempoAlias = ""
removeSilenceAtStart = False
nvdaAddonPath = ""
rhvoiceDllPath = ""
# PollyPro is not working
forceTTSMP3Usage = True

# Default write command
writeCommandChar = ord('W')

#FLASH_WRITE_SIZE = 2

PlatformsNames = [ "GD-77", "GD-77S", "DM-1801", "RD-5R", "DM-1801A", "MD-9600", "MD-UV380", "MD-380", "DM-1701", "MD-2017" ]

class PlatformModels(enum.Enum):
    PLATFORM_UNKNOWN = -1
    PLATFORM_GD77 = 0
    PLATFORM_GD77S = 1
    PLATFORM_DM1801 = 2
    PLATFORM_RD5R = 3
    PLATFORM_DM1801A = 4
    PLATFORM_MD9600 = 5
    PLATFORM_MDUV380 = 6
    PLATFORM_MD380 = 7
    PLATFORM_DM1701 = 8
    PLATFORM_MD2017 = 9

    def __int__(self):
        return self.value

class RadioInfoFeatures(enum.Enum):
    SCREEN_INVERTED = (1 << 0)
    DMRID_USES_VOICE_PROMPTS = (1 << 1)
    VOICE_PROMPTS_AVAILABLE = (1 << 2)

    def __int__(self):
        return self.value

class RadioInfoStruct(Structure):
    _pack_ = 1
    _fields_ = [('structVersion', c_uint),
                ('radioType', c_uint),
                ('gitRevision', c_char * 16),
                ('buildDateTime', c_char * 16),
                ('flashId', c_uint),
                ('features', c_ushort)]

platformModel = PlatformModels.PLATFORM_UNKNOWN
radioInfo = None;

###
# Check feature bit from RadioInfo's feature
###
def RadioInfoIsFeatureSet(feature):
    v = int(radioInfo.features)
    f = int(feature)

    if ((v & f) != 0):
        return True

    return False

###
# Read the RadioInfo, then fill the global structure
###
def readRadioInfo(ser):
    DataModeReadRadioInfo = 9
    sendbuffer = [0x0] * 8
    readbuffer = [0x0] * 64
    totalLength = 0
    radioInfoBuffer = []
    size = 8

    ser.flush()

    print("Read RadioInfo...")
    sendbuffer[0] = ord('R')
    sendbuffer[1] = DataModeReadRadioInfo
    sendbuffer[2] = 0
    sendbuffer[3] = 0
    sendbuffer[4] = 0
    sendbuffer[5] = 0
    sendbuffer[6] = ((size >> 8) & 0xFF);
    sendbuffer[7] = ((size >> 0) & 0xFF);

    ret = ser.write(sendbuffer)
    if (ret != 8):
        print("ERROR: write() wrote " + ret + " bytes")
        return False

    while (ser.in_waiting == 0):
        time.sleep(0.2)

    readbuffer = ser.read(ser.in_waiting)

    header = ord('R')

    if (readbuffer[0] == header):
        totalLength = (readbuffer[1] << 8) + (readbuffer[2] << 0)
        radioInfoBuffer[0:] = readbuffer[3:]

    else:
        return False

    if (totalLength > 0):
        ## Check about RadioInfo version and upgrade if possible
        ## Latest version is 0x03
        if (radioInfoBuffer[0] == 0x01):
            radioInfoBuffer += [0x00, 0x00] ## features  set to 0
        elif (radioInfoBuffer[0] == 0x02):
            radioInfoBuffer += [0x00]; ## convert old screenInverted to features

        global radioInfo
        radioInfo = RadioInfoStruct.from_buffer(bytearray(radioInfoBuffer))

        ##print(radioInfoBuffer)
        #print("   * structVersion:", radioInfo.structVersion)
        #print("   * radioType:", radioInfo.radioType)
        #print("   * gitRevision:", radioInfo.gitRevision.decode("utf-8"))
        #print("   * buildDateTime:", radioInfo.buildDateTime.decode("utf-8"))
        #print("   * flashId:", hex(radioInfo.flashId))
        #print("   * features:", hex(radioInfo.features))

        global platformModel
        platformModel = PlatformModels(radioInfo.radioType)

        return True

    return False

def serialInit(serialDev):
    ser = serial.Serial()
    ser.port = serialDev
    ser.baudrate = 115200
    ser.bytesize = serial.EIGHTBITS
    ser.parity = serial.PARITY_NONE
    ser.stopbits = serial.STOPBITS_ONE
    ##
    ## Non-blocking read/write
    ser.timeout = 0
    ser.write_timeout = 0
    ser.read_timeout = 0
    ##
    ##
    #ser.xonxoff = 0
    #ser.rtscts = 0

    try:
        ser.open()
    except serial.SerialException as err:
        print(str(err))
        sys.exit(1)
    return ser

def getMemoryArea(ser,buf,mode,bufStart,radioStart,length):
    snd = bytearray(FLASH_SEND_SIZE)
    snd[0] = ord('R')
    snd[1] = mode
    bufPos = bufStart
    radioPos = radioStart
    remaining = length
    while (remaining > 0):
        batch = min(remaining, MAX_TRANSFER_SIZE)

        snd[2] = (radioPos >> 24) & 0xFF
        snd[3] = (radioPos >> 16) & 0xFF
        snd[4] = (radioPos >>  8) & 0xFF
        snd[5] = (radioPos >>  0) & 0xFF
        snd[6] = (batch >> 8) & 0xFF
        snd[7] = (batch >> 0) & 0xFF

        ret = ser.write(snd)

        while (ser.out_waiting > 0):
            time.sleep(0)

        time.sleep(0.001) ## Give it a little bit of time to encode

        while (ser.in_waiting == 0):
            time.sleep(0)

        rcv = ser.read(ser.in_waiting)
        if (rcv[0] == snd[0]):
            gotBytes = (rcv[1] << 8) + rcv[2]
            for i in range(0,gotBytes):
                buf[bufPos] = rcv[i+3]
                bufPos += 1
            radioPos += gotBytes
            remaining -= gotBytes
        else:
            sys.exit("ABORT: Read ERROR (error at rcv[0]: " + str(rcv[0]) + ")")

    return True

def sendCommand(ser,commandNumber, x_or_command_option_number, y, iSize, alignment, isInverted, message):
    # snd allocation? len 64 or 32? or 23?
    snd = bytearray(7 + 21)
    snd[0] = ord('C')
    snd[1] = commandNumber
    snd[2] = x_or_command_option_number
    snd[3] = y
    snd[4] = iSize
    snd[5] = alignment
    snd[6] = isInverted
    # copy message to snd[7] (max 16 bytes)
    i = 7
    for c in message:
        if (i > 7+21-1):
            break
        snd[i] = ord(c)
        i += 1
    ser.flush()
    ret = ser.write(snd)
    if (ret != 7 + 21): # length?
        print("ERROR: write() wrote " + str(ret) + " bytes")
        return False
    while (ser.in_waiting == 0):
        time.sleep(0)
    rcv = ser.read(ser.in_waiting)
    return len(rcv) > 2 and rcv[1] == snd[1]

def wavSendData(ser,buf,radioStart,length):
    snd = bytearray(MAX_USB_TRANSFERT_SIZE)
    snd[0] = writeCommandChar
    snd[1] = 7#data type 7
    bufPos = 0
    radioPos = radioStart
    remaining = length
    while (remaining > 0):
        transferSize = min(remaining, MAX_TRANSFER_SIZE)

        snd[2] = (radioPos >> 24) & 0xFF
        snd[3] = (radioPos >> 16) & 0xFF
        snd[4] = (radioPos >>  8) & 0xFF
        snd[5] = (radioPos >>  0) & 0xFF
        snd[6] = (transferSize >>  8) & 0xFF
        snd[7] = (transferSize >>  0) & 0xFF
        snd[FLASH_SEND_SIZE:FLASH_SEND_SIZE + transferSize] = buf[bufPos:bufPos + transferSize]

        ## NOTE: it's not possible to specify the number of bytes to be written, hence a new tailored buffer is needed
        xmitBuffer = snd[0:FLASH_SEND_SIZE + transferSize]

        ret = ser.write(xmitBuffer)

        while (ser.out_waiting > 0):
            time.sleep(0)

        while (ser.in_waiting == 0):
            time.sleep(0)

        rcv = ser.read(ser.in_waiting)
        if (rcv[0] != snd[0]):
            sys.exit("ABORT: Send ERROR: at " + str(radioPos))

        bufPos += transferSize
        radioPos += transferSize
        remaining -= transferSize

    return True

def convert2AMBE(ser,infile,outfile):
    with open(infile,'rb') as f:
        ambBuf = bytearray(16 * 1024)# arbitary 16k buffer
        buf = bytearray(f.read())
        f.close();
        sendCommand(ser,1, 0, 0, 0, 0, 0, "") # Clear Screen
        sendCommand(ser,2, 0, 0, 2, 1, 0, "Tool") # Write line at line #0, front size 3, centered
        sendCommand(ser,2, 0, 16, 3, 1, 0, "Compress To AMBE") # Write line at line #16, front size 3, centered
        sendCommand(ser,2, 0, 39, 0, 1, 0, ntpath.basename(infile)[:-4]) # Write prompt name line at line #32, front size 0 (6x8 regular), centered
        sendCommand(ser,3, 0, 0, 0, 0, 0, "") # Render the screen
        wavBufPos = 0

        bufLen = len(buf)
        ambBufPos=0;
        ambFrameBuf = bytearray(27)
        startPos=0
        #if (infile[0:11] !="PROMPT_SPACE"):
        #    stripSilence = True;

        if (removeSilenceAtStart==True):
            while (startPos<len(buf) and  buf[startPos]==0 and buf[(startPos+1)]==0):
               startPos = startPos + 2;
            if (startPos == len(buf)):
                startPos = 0

        print("Compress to AMBE " + infile + " pos:+" + str(startPos));

        wavBufPos = startPos

        while (wavBufPos < bufLen):
            #print('.', end='')
            sendCommand(ser,6, 6, 0, 0, 0, 0,  "") # soundInit()
            transferLen = min(960, (bufLen - wavBufPos))
            #print("sent " + str(transferLen));
            wavSendData(ser, buf[wavBufPos:wavBufPos + transferLen], 0, transferLen)
            time.sleep(0.005)
            getMemoryArea(ser, ambFrameBuf, 8, 0, 0, 27) # mode 8 is read from AMBE
            ambBuf[ambBufPos:ambBufPos+27] = ambFrameBuf
            wavBufPos = wavBufPos + 960
            ambBufPos = ambBufPos + 27

        with open(outfile,'wb') as f:
            f.write(ambBuf[0:ambBufPos])

        #print("")#newline


def convertToRaw(inFile,outFile):
    print("ConvertToRaw "+ inFile + " -> " + outFile + " gain="+gain + " tempo="+atempo)
    callArgs = ['ffmpeg','-y','-i', inFile,'-filter:a','atempo=+'+atempo+',volume='+gain+'dB','-ar','8000','-f','s16le',outFile]
    if os.name == 'nt':
        subprocess.call(callArgs, creationflags=CREATE_NO_WINDOW)#'-af','silenceremove=1:0:-50dB'
    elif os.name == 'posix':
        subprocess.call(callArgs)#'-af','silenceremove=1:0:-50dB'


def parseSimpleInfo(text):
    values = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"')
    return values


def safeExtractZip(zipPath, targetDir):
    targetAbs = os.path.abspath(targetDir)
    with zipfile.ZipFile(zipPath, "r") as zf:
        for member in zf.infolist():
            name = member.filename.replace("\\", "/")
            if name.startswith("/") or name.startswith("../") or "/../" in name:
                raise RuntimeError("Unsafe path in add-on archive: " + member.filename)
            dest = os.path.abspath(os.path.join(targetAbs, *name.split("/")))
            if not (dest == targetAbs or dest.startswith(targetAbs + os.path.sep)):
                raise RuntimeError("Unsafe path in add-on archive: " + member.filename)
        zf.extractall(targetAbs)


def inspectNvdaAddon(addonPath):
    if not addonPath:
        raise RuntimeError("No NVDA add-on path was provided.")
    if not os.path.exists(addonPath):
        raise RuntimeError("NVDA add-on file not found: " + addonPath)
    try:
        with zipfile.ZipFile(addonPath, "r") as zf:
            names = {name.replace("\\", "/") for name in zf.namelist()}
            if "data/voice.info" not in names or "data/voice.params" not in names:
                raise RuntimeError("This .nvda-addon is not an RHVoice voice package. Expected data/voice.info and data/voice.params.")
            if not any(name.startswith("langdata/") for name in names):
                raise RuntimeError("This RHVoice voice add-on does not contain langdata. Add a matching RHVoice language add-on or use a complete voice package.")
            manifest = {}
            voice = {}
            if "manifest.ini" in names:
                manifest = parseSimpleInfo(zf.read("manifest.ini").decode("utf-8", errors="replace"))
            voice = parseSimpleInfo(zf.read("data/voice.info").decode("utf-8", errors="replace"))
            voiceName = voice.get("name") or manifest.get("name") or os.path.splitext(os.path.basename(addonPath))[0]
            language = voice.get("language", "")
            summary = manifest.get("summary", "")
            return {"name": voiceName, "language": language, "summary": summary}
    except zipfile.BadZipFile:
        raise RuntimeError("The selected .nvda-addon is not a valid ZIP archive: " + addonPath)


def preparedRhvoiceAddonDir(addonPath, workDir):
    info = inspectNvdaAddon(addonPath)
    with open(addonPath, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()[0:12]
    base = os.path.splitext(os.path.basename(addonPath))[0]
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", base).strip("._") or "nvda_addon"
    target = os.path.join(workDir, ".prompt_studio_nvda_addons", safe + "_" + digest)
    marker = os.path.join(target, ".extracted")
    if not os.path.exists(marker):
        os.makedirs(target, exist_ok=True)
        safeExtractZip(addonPath, target)
        with open(marker, "w", encoding="utf-8") as f:
            f.write(info.get("name", "") + "\n")
    return target, info


def findRhvoiceDll(explicitPath=""):
    candidates = []
    if explicitPath:
        candidates.append(explicitPath)
    envPath = os.environ.get("RHVOICE_DLL", "").strip()
    if envPath:
        candidates.append(envPath)
    bases = []
    if getattr(sys, "_MEIPASS", None):
        bases.append(sys._MEIPASS)
    bases.append(application_base_dir())
    for base in bases:
        candidates.extend([
            os.path.join(base, "RHVoice.dll"),
            os.path.join(base, "rhvoice", "RHVoice.dll"),
            os.path.join(base, "lib", "x64", "RHVoice.dll"),
        ])
    appdata = os.environ.get("APPDATA", "")
    if appdata:
        for nvdaName in ["NVDA", "nvda"]:
            candidates.append(os.path.join(appdata, nvdaName, "addons", "RHVoice", "synthDrivers", "RHVoice", "lib", "x64", "RHVoice.dll"))
            candidates.append(os.path.join(appdata, nvdaName, "addons", "RHVoice", "synthDrivers", "RHVoice", "lib", "x86", "RHVoice.dll"))
    for candidate in candidates:
        if candidate and os.path.exists(candidate):
            return os.path.abspath(candidate)
    raise RuntimeError("RHVoice.dll was not found. Install the RHVoice NVDA add-on, set RHVOICE_DLL, or copy RHVoice.dll next to the program.")


class RHVoiceEngineStruct(Structure):
    pass


RHVoiceEnginePtr = POINTER(RHVoiceEngineStruct)


class RHVoiceMessageStruct(Structure):
    pass


RHVoiceMessagePtr = POINTER(RHVoiceMessageStruct)
RHVoiceSetSampleRateCallback = CFUNCTYPE(c_int, c_int, c_void_p)
RHVoicePlaySpeechCallback = CFUNCTYPE(c_int, POINTER(c_short), c_uint, c_void_p)
RHVoiceProcessMarkCallback = CFUNCTYPE(c_int, c_char_p, c_void_p)
RHVoiceWordCallback = CFUNCTYPE(c_int, c_uint, c_uint, c_void_p)
RHVoicePlayAudioCallback = CFUNCTYPE(c_int, c_char_p, c_void_p)
RHVoiceDoneCallback = CFUNCTYPE(None, c_void_p)


class RHVoiceCallbacks(Structure):
    _fields_ = [
        ("set_sample_rate", RHVoiceSetSampleRateCallback),
        ("play_speech", RHVoicePlaySpeechCallback),
        ("process_mark", RHVoiceProcessMarkCallback),
        ("word_starts", RHVoiceWordCallback),
        ("word_ends", RHVoiceWordCallback),
        ("sentence_starts", RHVoiceWordCallback),
        ("sentence_ends", RHVoiceWordCallback),
        ("play_audio", RHVoicePlayAudioCallback),
        ("done", RHVoiceDoneCallback),
    ]


class RHVoiceInitParams(Structure):
    _fields_ = [
        ("data_path", c_char_p),
        ("config_path", c_char_p),
        ("resource_paths", POINTER(c_char_p)),
        ("callbacks", RHVoiceCallbacks),
        ("options", c_uint),
    ]


class RHVoiceSynthParams(Structure):
    _fields_ = [
        ("voice_profile", c_char_p),
        ("absolute_rate", c_double),
        ("absolute_pitch", c_double),
        ("absolute_volume", c_double),
        ("relative_rate", c_double),
        ("relative_pitch", c_double),
        ("relative_volume", c_double),
        ("punctuation_mode", c_int),
        ("punctuation_list", c_char_p),
        ("capitals_mode", c_int),
        ("flags", c_int),
    ]


class RHVoiceFileSynthesizer:
    def __init__(self, resourceDirs, configDir, dllPath=""):
        self.dllPath = findRhvoiceDll(dllPath)
        self.lib = CDLL(self.dllPath)
        self.lib.RHVoice_get_version.restype = c_char_p
        self.lib.RHVoice_new_tts_engine.argtypes = (POINTER(RHVoiceInitParams),)
        self.lib.RHVoice_new_tts_engine.restype = RHVoiceEnginePtr
        self.lib.RHVoice_delete_tts_engine.argtypes = (RHVoiceEnginePtr,)
        self.lib.RHVoice_delete_tts_engine.restype = None
        self.lib.RHVoice_get_number_of_voice_profiles.argtypes = (RHVoiceEnginePtr,)
        self.lib.RHVoice_get_number_of_voice_profiles.restype = c_uint
        self.lib.RHVoice_get_voice_profiles.argtypes = (RHVoiceEnginePtr,)
        self.lib.RHVoice_get_voice_profiles.restype = POINTER(c_char_p)
        self.lib.RHVoice_new_message.argtypes = (RHVoiceEnginePtr, c_char_p, c_uint, c_int, POINTER(RHVoiceSynthParams), c_void_p)
        self.lib.RHVoice_new_message.restype = RHVoiceMessagePtr
        self.lib.RHVoice_speak.argtypes = (RHVoiceMessagePtr,)
        self.lib.RHVoice_speak.restype = c_int
        self.lib.RHVoice_delete_message.argtypes = (RHVoiceMessagePtr,)
        self.lib.RHVoice_delete_message.restype = None
        os.makedirs(configDir, exist_ok=True)
        self.sampleRate = 0
        self.chunks = []
        self._setSampleRateCb = RHVoiceSetSampleRateCallback(self._setSampleRate)
        self._playSpeechCb = RHVoicePlaySpeechCallback(self._playSpeech)
        self._processMarkCb = RHVoiceProcessMarkCallback(self._processMark)
        self._playAudioCb = RHVoicePlayAudioCallback(self._playAudio)
        self._doneCb = RHVoiceDoneCallback(self._done)
        encoded = [os.path.abspath(path).encode("utf-8") for path in resourceDirs if os.path.isdir(path)]
        if not encoded:
            raise RuntimeError("No RHVoice resource directories were found.")
        self._resourceArray = (c_char_p * (len(encoded) + 1))(*(encoded + [None]))
        callbacks = RHVoiceCallbacks(
            self._setSampleRateCb,
            self._playSpeechCb,
            self._processMarkCb,
            cast(None, RHVoiceWordCallback),
            cast(None, RHVoiceWordCallback),
            cast(None, RHVoiceWordCallback),
            cast(None, RHVoiceWordCallback),
            self._playAudioCb,
            self._doneCb,
        )
        initParams = RHVoiceInitParams(
            None,
            os.path.abspath(configDir).encode("utf-8"),
            self._resourceArray,
            callbacks,
            0,
        )
        self.engine = self.lib.RHVoice_new_tts_engine(byref(initParams))
        if not self.engine:
            raise RuntimeError("RHVoice initialization failed.")
        self.voiceProfiles = self._readVoiceProfiles()
        if not self.voiceProfiles:
            raise RuntimeError("RHVoice did not report any voice profiles for the selected add-on.")
        version = self.lib.RHVoice_get_version()
        print("RHVoice engine: " + (version.decode("utf-8", errors="replace") if version else "unknown") + " (" + self.dllPath + ")")
        print("RHVoice profiles: " + ", ".join(self.voiceProfiles))

    def _readVoiceProfiles(self):
        count = self.lib.RHVoice_get_number_of_voice_profiles(self.engine)
        native = self.lib.RHVoice_get_voice_profiles(self.engine)
        return [native[i].decode("utf-8", errors="replace") for i in range(count)]

    def close(self):
        if getattr(self, "engine", None):
            self.lib.RHVoice_delete_tts_engine(self.engine)
            self.engine = None

    def _setSampleRate(self, sampleRate, userData):
        self.sampleRate = int(sampleRate)
        return 1

    def _playSpeech(self, samples, count, userData):
        self.chunks.append(string_at(samples, int(count) * sizeof(c_short)))
        return 1

    def _processMark(self, name, userData):
        return 1

    def _playAudio(self, path, userData):
        return 1

    def _done(self, userData):
        return None

    def synthesizeToWav(self, text, wavPath, requestedProfile=""):
        profile = requestedProfile if requestedProfile in self.voiceProfiles else self.voiceProfiles[0]
        self.sampleRate = 0
        self.chunks = []
        encodedText = text.encode("utf-8", errors="ignore")
        params = RHVoiceSynthParams(
            profile.encode("utf-8"),
            0,
            0,
            0,
            1,
            1,
            1,
            0,
            None,
            0,
            0,
        )
        msg = self.lib.RHVoice_new_message(self.engine, encodedText, len(encodedText), 0, byref(params), None)
        if not msg:
            raise RuntimeError("RHVoice could not create a message for text: " + text)
        try:
            result = self.lib.RHVoice_speak(msg)
        finally:
            self.lib.RHVoice_delete_message(msg)
        if result != 1 or not self.chunks:
            raise RuntimeError("RHVoice synthesis failed for text: " + text)
        os.makedirs(os.path.dirname(os.path.abspath(wavPath)), exist_ok=True)
        with wave.open(wavPath, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(self.sampleRate or 24000)
            wf.writeframes(b"".join(self.chunks))
        return profile


def synthesizeRhvoiceForWordList(filename, voiceName, addonPath, dllPath=""):
    print("Using RHVoice NVDA add-on: " + addonPath)
    addonDir, addonInfo = preparedRhvoiceAddonDir(addonPath, os.getcwd())
    print("RHVoice add-on voice: " + addonInfo.get("name", "unknown") + " " + addonInfo.get("language", ""))
    resourceDirs = [
        os.path.join(addonDir, "data"),
        os.path.join(addonDir, "langdata"),
        os.path.join(addonDir, "lang2data"),
    ]
    configDir = os.path.join(os.getcwd(), ".prompt_studio_rhvoice_config")
    ensureVoiceFolders(voiceName)
    synth = RHVoiceFileSynthesizer(resourceDirs, configDir, dllPath)
    try:
        requestedProfile = voiceName.strip()
        with open(filename, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(filter(lambda row: row[0] != '#', csvfile))
            for row in reader:
                promptName = row['PromptName'].strip()
                promptText = row['PromptSpeechPrefix'].strip() + row['PromptText'] + row['PromptSpeechPostfix'].strip()
                wavFileName = voiceName + os.path.sep + promptName + ".wav"
                rawFileName = voiceName + os.path.sep + "tempo_" + atempo + os.path.sep + promptName + ".raw"
                ambeFileName = voiceName + os.path.sep + "tempo_" + atempo + os.path.sep + promptName + ".amb"
                if (not os.path.exists(wavFileName)) or overwrite == True:
                    usedProfile = synth.synthesizeToWav(promptText, wavFileName, requestedProfile)
                    print("RHVoice: " + promptName + " -> " + wavFileName + " profile=" + usedProfile)
                if (not os.path.exists(rawFileName)) or overwrite == True:
                    convertToRaw(wavFileName, rawFileName)
                    if os.path.exists(ambeFileName):
                        os.remove(ambeFileName)
    finally:
        synth.close()

def downloadPollyPro(voiceName,fileStub,promptText,speechSpeed):
    global atempo
    retval=True
    hasDownloaded = False
    myobj = {'text-input': promptText,
             'voice':voiceName,
             'format':'mp3',# mp3 or ogg_vorbis or json
             'frequency':'22050',
             'effect':speechSpeed}

    data = urllib.parse.urlencode(myobj)
    data = data.encode('ascii')

    mp3FileName = voiceName + os.path.sep + fileStub + ".mp3"
    rawFileName = voiceName + os.path.sep + "tempo_" + atempo + os.path.sep + fileStub + ".raw"
    ambeFileName = voiceName + os.path.sep + "tempo_" + atempo + os.path.sep + fileStub + ".amb"

    if (not os.path.exists(mp3FileName) or overwrite==True):
        with urllib.request.urlopen("https://voicepolly.pro/speech-converter.php", data) as f:
            resp = f.read().decode('utf-8')
            print("PollyPro: Downloading synthesised speech for text: \"" + promptText + "\" -> " + mp3FileName)
            if resp.endswith('.mp3'):
                with urllib.request.urlopen(resp) as response, open(mp3FileName, 'wb') as out_file:
                    audioData = response.read() # a `bytes` object
                    out_file.write(audioData)
                    hasDownloaded = True
                    retval = True
            else:
                print("Error requesting sound " + resp)
                retval=False
#    else:
#        print("Download skipping " + file_name)

    if (hasDownloaded == True or not os.path.exists(rawFileName) or overwrite == True):
        convertToRaw(mp3FileName,rawFileName)
        if (os.path.exists(ambeFileName)):
            os.remove(ambeFileName)# ambe file is now out of date, so delete it

    return retval

def downloadTTSMP3(voiceName,fileStub,promptText):
    global atempo
    myobj = {'msg': promptText,
             'lang':voiceName,
             'source':'ttsmp3.com'}

    data = urllib.parse.urlencode(myobj)
    myStr = str.replace(data,"+","%20") #hacky fix because urlencode is not encoding spaces to %20
    data = myStr.encode('ascii')

    mp3FileName = voiceName + os.path.sep + fileStub + ".mp3"
    rawFileName = voiceName + os.path.sep + "tempo_" + atempo + os.path.sep + fileStub + ".raw"
    ambeFileName = voiceName + os.path.sep + "tempo_" + atempo + os.path.sep + fileStub + ".amb"

    hasDownloaded = False

    if (not os.path.exists(mp3FileName) or overwrite==True):
        print("Download TTSMP3 " +  promptText)

        with urllib.request.urlopen("https://ttsmp3.com/makemp3_new.php", data) as f:
            resp = f.read().decode('utf-8')
            print("TTSMP3: Downloading synthesised speech for text: \"" + promptText + "\" -> " + mp3FileName)
            print(resp)
            data = json.loads(resp)
            if (data['Error'] == 0):
                print(data['URL'])
                # Download the file from `url` and save it locally under `file_name`:
                with urllib.request.urlopen(data['URL']) as response, open(mp3FileName, 'wb') as out_file:
                    mp3data = response.read() # a `bytes` object
                    out_file.write(mp3data)
                    ## need to resample to 8kHz sample rate because ttsmp3 files are 22.05kHz
                    out_file.close()
                    hasDownloaded = True

            else:
                print("Error requesting sound")
                return False

    if (hasDownloaded == True or not os.path.exists(rawFileName) or overwrite == True):
        convertToRaw(mp3FileName,rawFileName)
        if (os.path.exists(ambeFileName)):
            os.remove(ambeFileName)# ambe file is now out of date, so delete it

    return True

def downloadSpeechForWordList(filename,voiceName):
    retval = True
    speechSpeed="normal"

    with open(filename,"r",encoding='utf-8') as csvfile:
        reader = csv.DictReader(filter(lambda row: row[0]!='#', csvfile))
        for row in reader:
            promptName = row['PromptName'].strip()

            speechPrefix = row['PromptSpeechPrefix'].strip()

            ## PollyPro is not working.
            if ((forceTTSMP3Usage == False) and (speechPrefix != "") and False):
                #Use VoicePolly as its not a special SSML that it doesnt handle
                if (speechPrefix.find("<prosody rate=")!=-1):
                    matchObj = re.search(r'\".*\"',speechPrefix)
                    if (matchObj):
                        speechSpeed = matchObj.group(0)[1:-1]

                downloadPollyPro(voiceName, promptName, row['PromptText'], speechSpeed)
            else:
                promptTTSText = row['PromptSpeechPrefix'].strip() +  row['PromptText'] + row['PromptSpeechPostfix'].strip()

                if (downloadTTSMP3(voiceName,promptName,promptTTSText)==False):
                    retval=False
                    break

    return retval

def encodeFile(ser,fileStub):
    if ((not os.path.exists(fileStub+".amb")) or overwrite==True):
        convert2AMBE(ser,fileStub+".raw",fileStub+".amb")
        #os.remove(fileStub+".raw")
##    else:
##       print("Encode skipping " + fileStub)

def encodeWordList(ser,filename,voiceName,forceReEncode):
    global atempo

    if (readRadioInfo(ser)):
        if (platformModel == PlatformModels.PLATFORM_MD9600) or (platformModel == PlatformModels.PLATFORM_MDUV380) or (platformModel == PlatformModels.PLATFORM_MD380) or (platformModel == PlatformModels.PLATFORM_DM1701) or (platformModel == PlatformModels.PLATFORM_MD2017):
            global writeCommandChar
            writeCommandChar = ord('X')

        print("Encoding using a {}".format(PlatformsNames[int(platformModel)]))

        with open(filename,"r",encoding='utf-8') as csvfile:
            sendCommand(ser,0, 0, 0, 0, 0, 0, "") # show CPS screen as this disables the radio etc
            sendCommand(ser,1, 0, 0, 0, 0, 0, "") # Clear Screen
            sendCommand(ser,3, 0, 0, 0, 0, 0, "") # Render the screen
            sendCommand(ser,6, 5, 0, 0, 0, 0,  "") # codecInitInternalBuffers()
            reader = csv.DictReader(filter(lambda row: row[0]!='#', csvfile))
            for row in reader:
                promptName = row['PromptName'].strip()
                fileStub = voiceName + os.path.sep + "tempo_" + atempo + os.path.sep + promptName


                encodeFile(ser,fileStub)

            sendCommand(ser,5, 0, 0, 0, 0, 0, "") # close CPS screen
    else:
        print("ERROR: unable to retrieve RadioInfo.")
        sys.exit(1)

def buildDataPack(filename,voiceName,outputFileName):
    flavors = [ "UV380-like", "monochrome" ]
    for flavor in flavors:
        print("Building " + flavor + " ...")
        promptsDict={}#create an empty dictionary
        with open(filename,"r",encoding='utf-8') as csvfile:
            reader = csv.DictReader(filter(lambda row: row[0]!='#', csvfile))
            for row in reader:
                promptName = row['PromptName'].strip()
                if (((flavor == "monochrome") and (promptName.startswith("theme_"))) == False):
                    infile = voiceName + os.path.sep + "tempo_" + atempo + os.path.sep + promptName + ".amb"
                    with open(infile,'rb') as f:
                        promptsDict[promptName] = bytearray(f.read())
                        f.close()
        MAX_PROMPTS = (331 if (flavor == "monochrome") else 368) ## 10 free each as of 2023 09 22
        headerTOCSize = (MAX_PROMPTS * 4) + 4 + 4
        outBuf = bytearray(headerTOCSize)
        outBuf[0:3]  = bytes([0x56, 0x50, 0x00, 0x00])#Magic number
        outBuf[4:7]  = bytes([(0x08 if (flavor == "monochrome") else 0x09), 0x00, 0x00, 0x00])#Version number
        outBuf[8:11] = bytes([0x00, 0x00, 0x00, 0x00])#First prompt audio is at offset zero
        bufPos=12;
        cumulativelength=0;
        for prompt in promptsDict:
            cumulativelength = cumulativelength + len(promptsDict[prompt]);
            outBuf[bufPos+3] = (cumulativelength >> 24) & 0xFF
            outBuf[bufPos+2] = (cumulativelength >> 16) & 0xFF
            outBuf[bufPos+1] = (cumulativelength >>  8) & 0xFF
            outBuf[bufPos+0] = (cumulativelength >>  0) & 0xFF
            bufPos = bufPos + 4

        #outputFileName = voiceName+'/voice_prompts_'+voiceName+'.bin'
        filenameVPR, fileExtension = os.path.splitext(outputFileName)
        flavoredFilename = filenameVPR + "_" + flavor + fileExtension
        with open(flavoredFilename, 'wb') as f:
            f.write(outBuf[0:headerTOCSize])#Should be headerTOCSize
            for prompt in promptsDict:
                f.write(promptsDict[prompt])

        print("Built voice pack " + flavoredFilename);

        ## Check file size
        fileSize = os.path.getsize(flavoredFilename)
        if fileSize > VOICE_PROMPTS_SIZE_MAX:
            errorMsg = "ERROR: VPR file '{}' is too big ({} bytes, but max is {} bytes, delta: {} bytes). File deleted.".format(flavoredFilename, fileSize, VOICE_PROMPTS_SIZE_MAX, (fileSize - VOICE_PROMPTS_SIZE_MAX))
            print(errorMsg)
            with open(r"../../LanguagesFilesDeleted.txt", "a") as fErrorLog:
                fErrorLog.write(errorMsg)
                fErrorLog.write("\n")
            os.remove(flavoredFilename)


def usage(message=""):
    print(PROGRAM_NAME + " v" + PROGRAM_VERSION)
    if (message != ""):
        print()
        print(message)
        print()

    print("Usage:  " + ntpath.basename(sys.argv[0]) + " [OPTION]")
    print("")
    print("    -h Display this help text,")
    print("    -c Configuration file (csv) - using this overrides all other options")
    print("    -f=<worlist_csv_file> : Wordlist file. Required for all functions")
    print("    -n=<voice_name>       : Voice name for synthesised speech and temporary folder name")
    ##print("    -n=<Voice_name>       : Voice name for synthesised speech from Voicepolly.pro and temporary folder name")
    ##print("    -s                    : Download synthesised speech from Voicepolly.pro")
    print("    -T                    : Download synthesised speech from ttsmp3.com")
    print("    -N=<nvda_addon>       : Synthesize speech from an RHVoice .nvda-addon")
    print("    -L=<RHVoice.dll>      : Optional path to RHVoice.dll")
    print("    -e                    : Encode previous download synthesised speech files, using the GD-77")
    print("    -b                    : Build voice prompts data pack from Encoded spech files ")
    print("    -d=<device>           : Use the specified device as serial port,")
    print("    -o                    : Overwrite existing files")
    print("    -g=gain               : Audio level gain adjust in db.  Default is 0, but can be negative or positive numbers")
    print("    -t=tempo              : Audio tempo (from 0.5 to 2).  Default is {}".format(atempo))
    print("    -A=alias              : use alias instead of speed number into the resulting filename")
    print("    -r                    : Remove silence from beginning of audio files")
    print("")

def ffmpegAvailable():
    if os.name == 'nt':
        return str(shutil.which("ffmpeg.exe")).find("ffmpeg") != -1
    return str(shutil.which("ffmpeg")).find("ffmpeg") != -1

def ensureVoiceFolders(voiceName):
    if not os.path.exists(voiceName):
        print("Creating folder " + voiceName + " for voice files")
        os.mkdir(voiceName);

    tempoDir = voiceName + os.path.sep + "tempo_" + atempo
    if not os.path.exists(tempoDir):
        print("Creating folder " + tempoDir + " for temporary files")
        os.mkdir(tempoDir);

def main(argv=None):
    global overwrite
    global gain
    global atempo
    global atempoAlias
    global removeSilenceAtStart, forceTTSMP3Usage
    global nvdaAddonPath, rhvoiceDllPath

    if argv is None:
        argv = sys.argv[1:]

    fileName   = ""#wordlist_english.csv"
    outputName = ""#voiceprompts.bin"
    voiceName = ""#Matthew or Nicole etc
    configName = ""

    # Default tty
    if (platform.system() == 'Windows'):
        serialDev = "COM71"
    else:
        serialDev = "/dev/ttyACM0"
    #Automatically search for the OpenGD77 device port
    for port in serial.tools.list_ports.comports():
        if (port.description.find("OpenGD77")==0):
            #print("Found OpenGD77 on port "+port.device);
            serialDev = port.device

    # Command line argument parsing
    try:
        ##opts, args = getopt.getopt(sys.argv[1:], "hof:n:seb:d:c:g:Tt:")
        opts, args = getopt.getopt(argv, "hon:f:eb:d:c:g:Tt:A:rN:L:", ["help"])
    except getopt.GetoptError as err:
        print(str(err))
        usage("")
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            return 0
        elif opt in ("-f"):
            fileName = arg
        elif opt in ("-n"):
            voiceName = arg
        elif opt in ("-d"):
            serialDev = arg
        elif opt in ("-c"):
            configName = arg
        elif opt in ("-o"):
            overwrite = True
        elif opt in ("-g"):
            gain = arg
        elif opt in ("-r"):
            removeSilenceAtStart = True
        elif opt in ("-T"):
            forceTTSMP3Usage = True
        elif opt in ("-N"):
            nvdaAddonPath = arg
        elif opt in ("-L"):
            rhvoiceDllPath = arg
        elif opt in ('-t'):
            atempo = arg
        elif opt in ('-A'):
            atempoAlias = arg

    if (configName != "") and not os.path.exists(configName):
        usage("ERROR: Config file not found: " + configName)
        sys.exit(2)

    configNeedsDownload = False
    if (configName != ""):
        with open(configName,"r",encoding='utf-8') as csvfile:
            reader = csv.DictReader(filter(lambda row: row[0]!='#', csvfile))
            for row in reader:
                if row.get('Download', '').strip().lower() == 'y':
                    configNeedsDownload = True
                    break

    needsFfmpeg = configNeedsDownload or any(opt in ("-T", "-N") for opt, arg in opts)
    if needsFfmpeg and not ffmpegAvailable():
        usage("ERROR: You must install ffmpeg. See https://www.ffmpeg.org/download.html")
        #webbrowser.open("https://www.ffmpeg.org/download.html")
        sys.exit(2)

    if (configName!=""):
        print("Using Config file: {}...".format(configName))

        with open(configName,"r",encoding='utf-8') as csvfile:
            reader = csv.DictReader(filter(lambda row: row[0]!='#', csvfile))
            for row in reader:
                wordlistFilename = row['Wordlist_file'].strip()
                voiceName = row['Voice_name'].strip()
                voicePackName = row['Voice_pack_name'].strip()
                download = row['Download'].strip()
                encode = row['Encode'].strip()
                createPack = row['Createpack'].strip()
                gain = row['Volume_change_db'].strip()
                rs = row['Remove_silence'].strip()
                cfg_atempo = row['Audio_tempo'].strip()
                cfg_nvda_addon = row.get('Nvda_addon_file', '').strip()
                cfg_rhvoice_dll = row.get('RHVoice_dll', '').strip()

                ## If Audio_tempo is not set, use the default value
                if cfg_atempo != '':
                    atempo = cfg_atempo

                ## Add audio tempo value to the filename
                voicePackName = voicePackName.replace('.vpr', '-' + (atempoAlias if len(atempoAlias) > 0 else atempo) + '.vpr');

                print("Processing " + wordlistFilename+" "+voiceName+" "+voicePackName)

                ensureVoiceFolders(voiceName)

                if (rs=='y' or rs=='Y'):
                    removeSilenceAtStart = True
                else:
                    removeSilenceAtStart = False

                if (download=='y' or download=='Y'):
                    if cfg_nvda_addon:
                        try:
                            synthesizeRhvoiceForWordList(wordlistFilename, voiceName, cfg_nvda_addon, cfg_rhvoice_dll)
                        except Exception as err:
                            usage("ERROR: " + str(err))
                            sys.exit(2)
                    else:
                        if (downloadSpeechForWordList(wordlistFilename,voiceName)==False):
                         sys.exit(2)

                if (encode=='y' or encode=='Y'):
                    ser = serialInit(serialDev)

                    encodeWordList(ser,wordlistFilename,voiceName,True)
                    if (ser.is_open):
                        ser.close()
                if (createPack=='y' or createPack=='Y'):
                    buildDataPack(wordlistFilename,voiceName,voicePackName)

        sys.exit(0)


    if (fileName=="" or voiceName==""):
        usage("ERROR: Filename and Voicename must be specified for all operations")
        sys.exit(2)

    if not os.path.exists(fileName):
        usage("ERROR: Wordlist file not found: " + fileName)
        sys.exit(2)

    ensureVoiceFolders(voiceName)

    if nvdaAddonPath:
        try:
            synthesizeRhvoiceForWordList(fileName, voiceName, nvdaAddonPath, rhvoiceDllPath)
        except Exception as err:
            usage("ERROR: " + str(err))
            sys.exit(2)
    else:
        for opt, arg in opts:
            if opt in ("-T"):
                if (downloadSpeechForWordList(fileName,voiceName)==False):
                    sys.exit(2)

    for opt, arg in opts:
        if opt in ("-e"):
            ser = serialInit(serialDev)
            encodeWordList(ser,fileName,voiceName,True)
            if (ser.is_open):
                ser.close()

    for opt, arg in opts:
        if opt in ("-b"):
            outputName = arg
            buildDataPack(fileName,voiceName,outputName)


def run_accessible_gui():
    try:
        return run_wx_gui()
    except ImportError as err:
        print("wxPython is not available, falling back to Tk GUI: " + str(err))
        return run_tk_gui()


def run_wx_gui():
    try:
        import wx
        import threading
        import queue
    except ImportError:
        raise
    except Exception as err:
        print("Unable to start GUI: " + str(err))
        usage("")
        return 2

    scriptPath = os.path.abspath(__file__)
    scriptDir = application_base_dir()
    processQueue = queue.Queue()
    currentProcess = {"proc": None}
    portDevices = []

    def consolePythonExecutable():
        exe = sys.executable
        if os.path.basename(exe).lower() == "pythonw.exe":
            candidate = os.path.join(os.path.dirname(exe), "python.exe")
            if os.path.exists(candidate):
                return candidate
        return exe

    def findFfmpegHint():
        found = shutil.which("ffmpeg.exe") if os.name == "nt" else shutil.which("ffmpeg")
        if found:
            return found
        candidates = [
            os.path.join(os.path.expanduser("~"), "Documents", "fmdx-webserver-src", "node_modules", "ffmpeg-static", "ffmpeg.exe"),
            os.path.join(scriptDir, "ffmpeg.exe")
        ]
        for candidate in candidates:
            if os.path.exists(candidate):
                return candidate
        return ""

    def findRhvoiceDllHint():
        try:
            return findRhvoiceDll("")
        except Exception:
            return ""

    app = wx.App(False)
    class FixedNameAccessible(wx.Accessible):
        def __init__(self, window, name, helpText):
            super().__init__(window)
            self._name = name
            self._helpText = helpText or name

        def GetName(self, childId):
            if childId == wx.ACC_SELF:
                return (wx.ACC_OK, self._name)
            return (wx.ACC_NOT_IMPLEMENTED, "")

        def GetHelpText(self, childId):
            if childId == wx.ACC_SELF:
                return (wx.ACC_OK, self._helpText)
            return (wx.ACC_NOT_IMPLEMENTED, "")

    frame = wx.Frame(None, title=PROGRAM_NAME + " - dostępne GUI", size=(1040, 820))
    frame.SetMinSize((920, 700))
    panel = wx.ScrolledWindow(frame)
    panel.SetScrollRate(8, 8)
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    panel.SetSizer(mainSizer)

    def setStatus(text):
        statusText.SetLabel(text)
        statusText.Wrap(-1)
        frame.SetStatusText(text)

    def appendLog(text):
        logCtrl.AppendText(text + os.linesep)

    def bindStatus(ctrl, text):
        ctrl.SetToolTip(text)
        ctrl.SetHelpText(text)
        ctrl.Bind(wx.EVT_SET_FOCUS, lambda event, msg=text: (setStatus(msg), event.Skip()))
        return ctrl

    def named(ctrl, name, helpText=None):
        ctrl.SetName(name)
        if helpText is None:
            helpText = name
        try:
            accessible = FixedNameAccessible(ctrl, name, helpText)
            ctrl.SetAccessible(accessible)
            ctrl._promptStudioAccessible = accessible
        except Exception:
            pass
        return bindStatus(ctrl, helpText)

    def addRow(parentSizer, labelText, ctrl, browseButton=None):
        row = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(panel, label=labelText)
        label.SetMinSize((210, -1))
        row.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 8)
        row.Add(ctrl, 1, wx.EXPAND | wx.RIGHT, 8)
        if browseButton is not None:
            row.Add(browseButton, 0, wx.ALIGN_CENTER_VERTICAL)
        parentSizer.Add(row, 0, wx.EXPAND | wx.ALL, 4)
        return row

    def fileDialog(title, wildcard, initialPath="", save=False):
        initialDir = os.path.dirname(initialPath) if initialPath else workDirCtrl.GetValue().strip()
        initialFile = os.path.basename(initialPath) if initialPath else ""
        style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT if save else wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        with wx.FileDialog(frame, title, defaultDir=initialDir or scriptDir, defaultFile=initialFile, wildcard=wildcard, style=style) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                return dialog.GetPath()
        return ""

    def browseFile(ctrl, title, wildcard, updateWorkDir=False):
        path = fileDialog(title, wildcard, ctrl.GetValue().strip())
        if path:
            ctrl.SetValue(path)
            if updateWorkDir:
                workDirCtrl.SetValue(os.path.dirname(path))

    def browseOutput():
        path = fileDialog("Wybierz nazwę pliku VPR", "Pakiet VPR (*.vpr)|*.vpr|Wszystkie pliki (*.*)|*.*", outputCtrl.GetValue().strip(), save=True)
        if path:
            outputCtrl.SetValue(path)

    def browseFolder(ctrl, title):
        initial = ctrl.GetValue().strip() or scriptDir
        with wx.DirDialog(frame, title, defaultPath=initial, style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                ctrl.SetValue(dialog.GetPath())

    def browseNvdaAddon():
        path = fileDialog("Wybierz dodatek NVDA z głosem RHVoice", "Dodatek NVDA (*.nvda-addon)|*.nvda-addon|Wszystkie pliki (*.*)|*.*", nvdaAddonCtrl.GetValue().strip())
        if not path:
            return
        nvdaAddonCtrl.SetValue(path)
        speechNvdaRadio.SetValue(True)
        try:
            info = inspectNvdaAddon(path)
            voiceText = voiceCtrl.GetValue().strip()
            if (not voiceText) or voiceText.lower() in ("polish", "voice"):
                voiceCtrl.SetValue(info.get("name", "RHVoice"))
            setStatus("Wybrano dodatek RHVoice: " + info.get("name", "") + " " + info.get("language", ""))
        except Exception as err:
            setStatus("Dodatek NVDA nie jest obsługiwanym głosem RHVoice.")
            wx.MessageBox(str(err), "Dodatek NVDA", wx.OK | wx.ICON_ERROR, frame)

    def refreshPorts():
        portDevices.clear()
        current = serialCtrl.GetValue().strip()
        listCtrl.Clear()
        try:
            for port in serial.tools.list_ports.comports():
                label = port.device
                if port.description:
                    label += " - " + port.description
                portDevices.append(port.device)
                listCtrl.Append(label)
                if not current and port.description.find("OpenGD77") == 0:
                    serialCtrl.SetValue(port.device)
                    current = port.device
        except Exception as err:
            appendLog("Nie udało się odczytać portów COM: " + str(err))
        if not serialCtrl.GetValue().strip() and portDevices:
            serialCtrl.SetValue(portDevices[0])
        setStatus("Odświeżono listę portów. Wpisz port ręcznie albo wybierz go z listy.")

    def selectPortFromList(event=None):
        selection = listCtrl.GetSelection()
        if selection != wx.NOT_FOUND and selection < len(portDevices):
            serialCtrl.SetValue(portDevices[selection])
            setStatus("Wybrano port " + portDevices[selection])

    def checkDependencies(event=None):
        messages = []
        messages.append("Python: " + consolePythonExecutable())
        messages.append("wxPython: OK (" + wx.version() + ")")
        try:
            import serial as serialModule
            messages.append("pyserial: OK (" + getattr(serialModule, "__version__", "wersja nieznana") + ")")
        except Exception as err:
            messages.append("pyserial: BŁĄD - " + str(err))

        ffmpegCandidate = ffmpegCtrl.GetValue().strip()
        if ffmpegCandidate and os.path.exists(ffmpegCandidate):
            messages.append("ffmpeg: OK (" + ffmpegCandidate + ")")
        elif ffmpegAvailable():
            messages.append("ffmpeg: OK w PATH")
        else:
            messages.append("ffmpeg: BRAK. Wybierz ffmpeg.exe albo dodaj ffmpeg do PATH.")

        addonCandidate = nvdaAddonCtrl.GetValue().strip()
        if addonCandidate:
            try:
                info = inspectNvdaAddon(addonCandidate)
                messages.append("NVDA/RHVoice add-on: OK (" + info.get("name", "unknown") + ")")
            except Exception as err:
                messages.append("NVDA/RHVoice add-on: ERROR - " + str(err))
        elif speechNvdaRadio.GetValue():
            messages.append("NVDA/RHVoice add-on: missing .nvda-addon path.")

        if speechNvdaRadio.GetValue() or addonCandidate or rhvoiceDllCtrl.GetValue().strip():
            try:
                dll = findRhvoiceDll(rhvoiceDllCtrl.GetValue().strip())
                messages.append("RHVoice.dll: OK (" + dll + ")")
            except Exception as err:
                messages.append("RHVoice.dll: ERROR - " + str(err))
        else:
            messages.append("RHVoice.dll: skipped because TTSMP3 is selected.")

        appendLog("Test zależności:")
        for message in messages:
            appendLog("  " + message)
        wx.MessageBox("\n".join(messages), "Test zależności", wx.OK | wx.ICON_INFORMATION, frame)

    def buildCommand():
        args = []
        if modeConfigRadio.GetValue():
            configPath = configCtrl.GetValue().strip()
            if not configPath:
                raise ValueError("Wybierz plik konfiguracyjny CSV.")
            args.extend(["-c", configPath])
        else:
            wordlist = wordlistCtrl.GetValue().strip()
            voiceName = voiceCtrl.GetValue().strip()
            if not wordlist:
                raise ValueError("Wybierz plik wordlist CSV.")
            if not voiceName:
                raise ValueError("Podaj nazwę głosu lub folderu głosu.")
            if not (downloadCheck.GetValue() or encodeCheck.GetValue() or buildCheck.GetValue()):
                raise ValueError("Zaznacz przynajmniej jedną operację: pobieranie, kodowanie albo budowanie VPR.")
            args.extend(["-f", wordlist, "-n", voiceName])
            if serialCtrl.GetValue().strip():
                args.extend(["-d", serialCtrl.GetValue().strip()])
            if downloadCheck.GetValue():
                if speechNvdaRadio.GetValue():
                    addonPath = nvdaAddonCtrl.GetValue().strip()
                    if not addonPath:
                        raise ValueError("Wybierz plik .nvda-addon z głosem RHVoice.")
                    args.extend(["-N", addonPath])
                    if rhvoiceDllCtrl.GetValue().strip():
                        args.extend(["-L", rhvoiceDllCtrl.GetValue().strip()])
                else:
                    args.append("-T")
            if encodeCheck.GetValue():
                args.append("-e")
            if buildCheck.GetValue():
                outputPath = outputCtrl.GetValue().strip()
                if not outputPath:
                    raise ValueError("Wybierz nazwę pliku wyjściowego VPR.")
                args.extend(["-b", outputPath])

        if overwriteCheck.GetValue():
            args.append("-o")
        if removeSilenceCheck.GetValue():
            args.append("-r")
        if gainCtrl.GetValue().strip():
            args.extend(["-g", gainCtrl.GetValue().strip()])
        if tempoCtrl.GetValue().strip():
            args.extend(["-t", tempoCtrl.GetValue().strip()])
        if aliasCtrl.GetValue().strip():
            args.extend(["-A", aliasCtrl.GetValue().strip()])
        return args

    def startRun(event=None):
        if currentProcess["proc"] is not None:
            wx.MessageBox("Builder już działa.", "Proces działa", wx.OK | wx.ICON_WARNING, frame)
            return
        try:
            args = buildCommand()
            workDir = workDirCtrl.GetValue().strip() or scriptDir
            if not os.path.isdir(workDir):
                raise ValueError("Folder roboczy nie istnieje: " + workDir)
        except Exception as err:
            wx.MessageBox(str(err), "Brak danych", wx.OK | wx.ICON_ERROR, frame)
            setStatus(str(err))
            return

        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        env["PYTHONUNBUFFERED"] = "1"
        ffmpegCandidate = ffmpegCtrl.GetValue().strip()
        if ffmpegCandidate and os.path.exists(ffmpegCandidate):
            env["PATH"] = os.path.dirname(ffmpegCandidate) + os.pathsep + env.get("PATH", "")
        if rhvoiceDllCtrl.GetValue().strip():
            env["RHVOICE_DLL"] = rhvoiceDllCtrl.GetValue().strip()

        if is_frozen_app():
            command = [sys.executable] + args
        else:
            command = [consolePythonExecutable(), "-u", scriptPath] + args
        appendLog("")
        appendLog("Start: " + " ".join(command))
        appendLog("Folder roboczy: " + workDir)
        setStatus("Builder działa. Log jest aktualizowany na bieżąco.")
        runButton.Enable(False)
        stopButton.Enable(True)

        def worker():
            try:
                proc = subprocess.Popen(
                    command,
                    cwd=workDir,
                    env=env,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    bufsize=1,
                    creationflags=(CREATE_NO_WINDOW if os.name == "nt" else 0)
                )
                currentProcess["proc"] = proc
                for line in proc.stdout:
                    processQueue.put(("log", line.rstrip("\r\n")))
                code = proc.wait()
                processQueue.put(("done", code))
            except Exception as err:
                processQueue.put(("error", str(err)))

        threading.Thread(target=worker, daemon=True).start()

    def stopRun(event=None):
        proc = currentProcess["proc"]
        if proc is None:
            return
        appendLog("Zatrzymuję proces...")
        setStatus("Zatrzymywanie procesu.")
        try:
            proc.terminate()
        except Exception as err:
            appendLog("Nie udało się zatrzymać procesu: " + str(err))

    def pumpQueue(event=None):
        try:
            while True:
                kind, payload = processQueue.get_nowait()
                if kind == "log":
                    appendLog(payload)
                elif kind == "done":
                    currentProcess["proc"] = None
                    runButton.Enable(True)
                    stopButton.Enable(False)
                    if payload == 0:
                        setStatus("Zakończono pomyślnie.")
                    else:
                        setStatus("Proces zakończył się błędem. Kod: " + str(payload))
                    appendLog("Koniec. Kod wyjścia: " + str(payload))
                elif kind == "error":
                    currentProcess["proc"] = None
                    runButton.Enable(True)
                    stopButton.Enable(False)
                    setStatus("Błąd uruchamiania.")
                    appendLog("Błąd uruchamiania: " + payload)
        except queue.Empty:
            pass

    def openWorkFolder(event=None):
        path = workDirCtrl.GetValue().strip() or scriptDir
        if os.path.isdir(path):
            os.startfile(path)

    def clearLog(event=None):
        logCtrl.Clear()
        setStatus("Log wyczyszczony.")

    def refreshModeState(event=None):
        configMode = modeConfigRadio.GetValue()
        for widget in configWidgets:
            widget.Enable(configMode)
        for widget in manualWidgets:
            widget.Enable(not configMode)
        setStatus("Tryb: " + ("plik konfiguracyjny CSV" if configMode else "ręczny"))

    def onClose(event):
        proc = currentProcess["proc"]
        if proc is not None:
            try:
                proc.terminate()
            except Exception:
                pass
        frame.Destroy()

    frame.CreateStatusBar()

    modeBox = wx.StaticBoxSizer(wx.VERTICAL, panel, "Tryb pracy")
    modeRow = wx.BoxSizer(wx.HORIZONTAL)
    modeManualRadio = named(wx.RadioButton(panel, label="Tryb ręczny", style=wx.RB_GROUP), "Tryb ręczny", "Tryb ręczny. Wybierasz wordlistę, głos, port i operacje.")
    modeConfigRadio = named(wx.RadioButton(panel, label="Plik konfiguracyjny CSV"), "Plik konfiguracyjny CSV", "Tryb pliku konfiguracyjnego CSV. Builder wykona operacje zapisane w CSV.")
    modeManualRadio.SetValue(True)
    modeRow.Add(modeManualRadio, 0, wx.RIGHT, 18)
    modeRow.Add(modeConfigRadio, 0)
    modeBox.Add(modeRow, 0, wx.ALL, 4)
    mainSizer.Add(modeBox, 0, wx.EXPAND | wx.ALL, 6)

    configBox = wx.StaticBoxSizer(wx.VERTICAL, panel, "Konfiguracja CSV")
    configCtrl = named(wx.TextCtrl(panel), "Plik konfiguracyjny CSV", "ścieżka do pliku konfiguracyjnego CSV.")
    configBrowse = named(wx.Button(panel, label="Wybierz..."), "Wybierz plik konfiguracyjny CSV")
    configBrowse.Bind(wx.EVT_BUTTON, lambda event: browseFile(configCtrl, "Wybierz plik konfiguracyjny", "CSV (*.csv)|*.csv|Wszystkie pliki (*.*)|*.*", True))
    addRow(configBox, "Plik konfiguracyjny:", configCtrl, configBrowse)
    mainSizer.Add(configBox, 0, wx.EXPAND | wx.ALL, 6)

    manualBox = wx.StaticBoxSizer(wx.VERTICAL, panel, "Tryb ręczny")
    wordlistCtrl = named(wx.TextCtrl(panel), "Wordlist CSV", "Plik CSV z kolumnami promptów.")
    wordlistBrowse = named(wx.Button(panel, label="Wybierz..."), "Wybierz wordlist CSV")
    wordlistBrowse.Bind(wx.EVT_BUTTON, lambda event: browseFile(wordlistCtrl, "Wybierz wordlist CSV", "CSV (*.csv)|*.csv|Wszystkie pliki (*.*)|*.*"))
    addRow(manualBox, "Wordlist CSV:", wordlistCtrl, wordlistBrowse)

    voiceCtrl = named(wx.TextCtrl(panel, value="Polish"), "Nazwa głosu", "Nazwa głosu i folderu na pliki audio.")
    addRow(manualBox, "Nazwa głosu:", voiceCtrl)

    outputCtrl = named(wx.TextCtrl(panel, value=os.path.join(scriptDir, "voice_prompts.vpr")), "Plik wynikowy VPR", "Bazowa nazwa pliku VPR. Program utworzy warianty UV380-like i monochrome.")
    outputBrowse = named(wx.Button(panel, label="Wybierz..."), "Wybierz plik wynikowy VPR")
    outputBrowse.Bind(wx.EVT_BUTTON, lambda event: browseOutput())
    addRow(manualBox, "Plik wynikowy VPR:", outputCtrl, outputBrowse)

    serialRow = wx.BoxSizer(wx.HORIZONTAL)
    serialLabel = wx.StaticText(panel, label="Port COM radia:")
    serialLabel.SetMinSize((210, -1))
    serialCtrl = named(wx.TextCtrl(panel, size=(120, -1)), "Port COM radia", "Port COM radia OpenGD77, na przykład COM5.")
    refreshPortsButton = named(wx.Button(panel, label="Odśwież porty"), "Odśwież porty")
    refreshPortsButton.Bind(wx.EVT_BUTTON, lambda event: refreshPorts())
    serialRow.Add(serialLabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 8)
    serialRow.Add(serialCtrl, 0, wx.RIGHT, 8)
    serialRow.Add(refreshPortsButton, 0)
    manualBox.Add(serialRow, 0, wx.EXPAND | wx.ALL, 4)

    listCtrl = named(wx.ListBox(panel, size=(-1, 90)), "Lista wykrytych portów", "Lista wykrytych portów. Strzałkami wybierz port.")
    listCtrl.Bind(wx.EVT_LISTBOX, selectPortFromList)
    manualBox.Add(listCtrl, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 4)

    opsRow = wx.BoxSizer(wx.HORIZONTAL)
    downloadCheck = named(wx.CheckBox(panel, label="Pobierz / syntezuj audio"), "Pobierz lub syntezuj audio")
    encodeCheck = named(wx.CheckBox(panel, label="Koduj AMBE w radiu"), "Koduj AMBE w radiu")
    buildCheck = named(wx.CheckBox(panel, label="Zbuduj VPR"), "Zbuduj plik VPR")
    buildCheck.SetValue(True)
    for ctrl in (downloadCheck, encodeCheck, buildCheck):
        opsRow.Add(ctrl, 0, wx.RIGHT, 18)
    manualBox.Add(opsRow, 0, wx.ALL, 4)

    sourceBox = wx.StaticBoxSizer(wx.VERTICAL, panel, "Źródło mowy przy pobieraniu")
    sourceRow = wx.BoxSizer(wx.HORIZONTAL)
    speechTtsRadio = named(wx.RadioButton(panel, label="TTSMP3.com", style=wx.RB_GROUP), "Źródło mowy TTSMP3.com", "Źródło mowy: internetowa usługa TTSMP3.")
    speechNvdaRadio = named(wx.RadioButton(panel, label="RHVoice z dodatku NVDA"), "Źródło mowy RHVoice z dodatku NVDA", "Źródło mowy: lokalny głos RHVoice z dodatku NVDA.")
    speechTtsRadio.SetValue(True)
    sourceRow.Add(speechTtsRadio, 0, wx.RIGHT, 18)
    sourceRow.Add(speechNvdaRadio, 0)
    sourceBox.Add(sourceRow, 0, wx.ALL, 4)

    nvdaAddonCtrl = named(wx.TextCtrl(panel), "Plik dodatku NVDA", "Plik .nvda-addon zawierający głos RHVoice.")
    nvdaAddonBrowse = named(wx.Button(panel, label="Wybierz..."), "Wybierz dodatek NVDA")
    nvdaAddonBrowse.Bind(wx.EVT_BUTTON, lambda event: browseNvdaAddon())
    addRow(sourceBox, "Dodatek NVDA:", nvdaAddonCtrl, nvdaAddonBrowse)

    rhvoiceDllCtrl = named(wx.TextCtrl(panel, value=findRhvoiceDllHint()), "RHVoice.dll", "Opcjonalna ścieżka do RHVoice.dll. Puste oznacza automatyczne wykrywanie.")
    rhvoiceDllBrowse = named(wx.Button(panel, label="Wybierz..."), "Wybierz RHVoice.dll")
    rhvoiceDllBrowse.Bind(wx.EVT_BUTTON, lambda event: browseFile(rhvoiceDllCtrl, "Wybierz RHVoice.dll", "RHVoice.dll|RHVoice.dll|DLL (*.dll)|*.dll|Wszystkie pliki (*.*)|*.*"))
    addRow(sourceBox, "RHVoice.dll:", rhvoiceDllCtrl, rhvoiceDllBrowse)
    manualBox.Add(sourceBox, 0, wx.EXPAND | wx.ALL, 4)
    mainSizer.Add(manualBox, 0, wx.EXPAND | wx.ALL, 6)

    optionsBox = wx.StaticBoxSizer(wx.VERTICAL, panel, "Opcje")
    workDirCtrl = named(wx.TextCtrl(panel, value=scriptDir), "Folder roboczy", "Folder roboczy dla plików tymczasowych i ścieżek względnych.")
    workDirBrowse = named(wx.Button(panel, label="Wybierz..."), "Wybierz folder roboczy")
    workDirBrowse.Bind(wx.EVT_BUTTON, lambda event: browseFolder(workDirCtrl, "Wybierz folder roboczy"))
    addRow(optionsBox, "Folder roboczy:", workDirCtrl, workDirBrowse)

    ffmpegCtrl = named(wx.TextCtrl(panel, value=findFfmpegHint()), "ffmpeg.exe", "ścieżka do ffmpeg.exe albo puste, jeśli ffmpeg jest w PATH.")
    ffmpegBrowse = named(wx.Button(panel, label="Wybierz..."), "Wybierz ffmpeg.exe")
    ffmpegBrowse.Bind(wx.EVT_BUTTON, lambda event: browseFile(ffmpegCtrl, "Wybierz ffmpeg.exe", "ffmpeg.exe|ffmpeg.exe|EXE (*.exe)|*.exe|Wszystkie pliki (*.*)|*.*"))
    addRow(optionsBox, "ffmpeg.exe:", ffmpegCtrl, ffmpegBrowse)

    audioRow = wx.BoxSizer(wx.HORIZONTAL)
    audioRow.Add(wx.StaticText(panel, label="Głośność dB:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 8)
    gainCtrl = named(wx.TextCtrl(panel, value=gain, size=(70, -1)), "Głośność dB", "Zmiana głośności w decybelach.")
    audioRow.Add(gainCtrl, 0, wx.RIGHT, 20)
    audioRow.Add(wx.StaticText(panel, label="Tempo:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 8)
    tempoCtrl = named(wx.TextCtrl(panel, value=atempo, size=(70, -1)), "Tempo", "Tempo audio od 0.5 do 2.")
    audioRow.Add(tempoCtrl, 0, wx.RIGHT, 20)
    audioRow.Add(wx.StaticText(panel, label="Alias tempa:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 8)
    aliasCtrl = named(wx.TextCtrl(panel, size=(120, -1)), "Alias tempa", "Opcjonalny alias tempa używany w nazwie pliku.")
    audioRow.Add(aliasCtrl, 0)
    optionsBox.Add(audioRow, 0, wx.ALL, 4)

    optionChecksRow = wx.BoxSizer(wx.HORIZONTAL)
    overwriteCheck = named(wx.CheckBox(panel, label="Nadpisuj istniejące pliki"), "Nadpisuj istniejące pliki")
    removeSilenceCheck = named(wx.CheckBox(panel, label="Usuń ciszę z początku"), "Usuń ciszę z początku")
    optionChecksRow.Add(overwriteCheck, 0, wx.RIGHT, 18)
    optionChecksRow.Add(removeSilenceCheck, 0)
    optionsBox.Add(optionChecksRow, 0, wx.ALL, 4)
    mainSizer.Add(optionsBox, 0, wx.EXPAND | wx.ALL, 6)

    buttonsRow = wx.BoxSizer(wx.HORIZONTAL)
    runButton = named(wx.Button(panel, label="Uruchom Alt+R"), "Uruchom builder")
    stopButton = named(wx.Button(panel, label="Zatrzymaj Alt+S"), "Zatrzymaj builder")
    depsButton = named(wx.Button(panel, label="Test zależności"), "Test zależności")
    openButton = named(wx.Button(panel, label="Otwórz folder"), "Otwórz folder roboczy")
    clearButton = named(wx.Button(panel, label="Wyczyść log"), "Wyczyść log")
    closeButton = named(wx.Button(panel, label="Zamknij"), "Zamknij program")
    stopButton.Enable(False)
    for ctrl in (runButton, stopButton, depsButton, openButton, clearButton, closeButton):
        buttonsRow.Add(ctrl, 0, wx.RIGHT, 8)
    mainSizer.Add(buttonsRow, 0, wx.EXPAND | wx.ALL, 6)

    statusBox = wx.StaticBoxSizer(wx.VERTICAL, panel, "Status i log")
    statusText = wx.StaticText(panel, label="Gotowe. Wybierz pliki i naciśnij Alt+R, aby uruchomić.")
    statusText.SetName("Status programu")
    statusBox.Add(statusText, 0, wx.EXPAND | wx.ALL, 4)
    logCtrl = named(wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2, size=(-1, 160)), "Log działania buildera", "Log działania buildera.")
    statusBox.Add(logCtrl, 1, wx.EXPAND | wx.ALL, 4)
    mainSizer.Add(statusBox, 1, wx.EXPAND | wx.ALL, 6)

    configWidgets = [configCtrl, configBrowse]
    manualWidgets = [
        wordlistCtrl, wordlistBrowse, voiceCtrl, outputCtrl, outputBrowse,
        serialCtrl, refreshPortsButton, listCtrl, downloadCheck, encodeCheck, buildCheck,
        speechTtsRadio, speechNvdaRadio, nvdaAddonCtrl, nvdaAddonBrowse, rhvoiceDllCtrl, rhvoiceDllBrowse
    ]

    modeManualRadio.Bind(wx.EVT_RADIOBUTTON, refreshModeState)
    modeConfigRadio.Bind(wx.EVT_RADIOBUTTON, refreshModeState)
    runButton.Bind(wx.EVT_BUTTON, startRun)
    stopButton.Bind(wx.EVT_BUTTON, stopRun)
    depsButton.Bind(wx.EVT_BUTTON, checkDependencies)
    openButton.Bind(wx.EVT_BUTTON, openWorkFolder)
    clearButton.Bind(wx.EVT_BUTTON, clearLog)
    closeButton.Bind(wx.EVT_BUTTON, lambda event: frame.Close())
    frame.Bind(wx.EVT_CLOSE, onClose)

    ID_RUN = wx.NewIdRef()
    ID_STOP = wx.NewIdRef()
    ID_LOG = wx.NewIdRef()
    ID_REFRESH = wx.NewIdRef()
    frame.Bind(wx.EVT_MENU, startRun, id=ID_RUN)
    frame.Bind(wx.EVT_MENU, stopRun, id=ID_STOP)
    frame.Bind(wx.EVT_MENU, lambda event: logCtrl.SetFocus(), id=ID_LOG)
    frame.Bind(wx.EVT_MENU, lambda event: refreshPorts(), id=ID_REFRESH)
    frame.SetAcceleratorTable(wx.AcceleratorTable([
        (wx.ACCEL_ALT, ord('R'), ID_RUN),
        (wx.ACCEL_ALT, ord('S'), ID_STOP),
        (wx.ACCEL_ALT, ord('L'), ID_LOG),
        (wx.ACCEL_NORMAL, wx.WXK_F5, ID_REFRESH),
    ]))

    timer = wx.Timer(frame)
    frame.Bind(wx.EVT_TIMER, pumpQueue, timer)
    timer.Start(100)

    refreshPorts()
    refreshModeState()
    panel.FitInside()
    frame.Show()
    wordlistCtrl.SetFocus()
    app.MainLoop()
    return 0

def run_tk_gui():
    try:
        import tkinter as tk
        from tkinter import filedialog, messagebox
        import threading
        import queue
    except Exception as err:
        print("Unable to start GUI: " + str(err))
        usage("")
        return 2

    scriptPath = os.path.abspath(__file__)
    scriptDir = application_base_dir()
    processQueue = queue.Queue()
    currentProcess = {"proc": None}

    def consolePythonExecutable():
        exe = sys.executable
        if os.path.basename(exe).lower() == "pythonw.exe":
            candidate = os.path.join(os.path.dirname(exe), "python.exe")
            if os.path.exists(candidate):
                return candidate
        return exe

    def findFfmpegHint():
        found = shutil.which("ffmpeg.exe") if os.name == "nt" else shutil.which("ffmpeg")
        if found:
            return found
        candidates = [
            os.path.join(os.path.expanduser("~"), "Documents", "fmdx-webserver-src", "node_modules", "ffmpeg-static", "ffmpeg.exe"),
            os.path.join(scriptDir, "ffmpeg.exe")
        ]
        for candidate in candidates:
            if os.path.exists(candidate):
                return candidate
        return ""

    def findRhvoiceDllHint():
        try:
            return findRhvoiceDll("")
        except Exception:
            return ""

    root = tk.Tk()
    root.title(PROGRAM_NAME + " - dostępne GUI")
    root.geometry("1040x820")
    root.minsize(920, 700)

    modeVar = tk.StringVar(value="manual")
    configPathVar = tk.StringVar()
    wordlistPathVar = tk.StringVar()
    voiceNameVar = tk.StringVar(value="Polish")
    outputPathVar = tk.StringVar(value=os.path.join(scriptDir, "voice_prompts.vpr"))
    workDirVar = tk.StringVar(value=scriptDir)
    serialPortVar = tk.StringVar()
    speechSourceVar = tk.StringVar(value="ttsmp3")
    nvdaAddonPathVar = tk.StringVar()
    rhvoiceDllPathVar = tk.StringVar(value=findRhvoiceDllHint())
    ffmpegPathVar = tk.StringVar(value=findFfmpegHint())
    gainVar = tk.StringVar(value=gain)
    tempoVar = tk.StringVar(value=atempo)
    aliasVar = tk.StringVar()
    downloadVar = tk.BooleanVar(value=False)
    encodeVar = tk.BooleanVar(value=False)
    buildVar = tk.BooleanVar(value=True)
    overwriteVar = tk.BooleanVar(value=False)
    removeSilenceVar = tk.BooleanVar(value=False)
    statusVar = tk.StringVar(value="Gotowe. Wybierz pliki i naciśnij Alt+R, aby uruchomić.")

    def appendLog(text):
        logText.configure(state="normal")
        logText.insert("end", text + "\n")
        logText.see("end")
        logText.configure(state="disabled")

    def setStatus(text):
        statusVar.set(text)
        root.update_idletasks()

    def describe(widget, text):
        widget.bind("<FocusIn>", lambda event: setStatus(text))

    def browseFile(var, title, filetypes):
        initial = var.get().strip()
        initialDir = os.path.dirname(initial) if initial else workDirVar.get().strip()
        path = filedialog.askopenfilename(title=title, initialdir=initialDir or scriptDir, filetypes=filetypes)
        if path:
            var.set(path)
            if var is configPathVar:
                workDirVar.set(os.path.dirname(path))

    def browseOutput():
        initial = outputPathVar.get().strip()
        path = filedialog.asksaveasfilename(
            title="Wybierz nazwę pliku VPR",
            initialdir=(os.path.dirname(initial) if initial else workDirVar.get().strip()) or scriptDir,
            initialfile=(os.path.basename(initial) if initial else "voice_prompts.vpr"),
            defaultextension=".vpr",
            filetypes=[("Pakiet VPR", "*.vpr"), ("Wszystkie pliki", "*.*")]
        )
        if path:
            outputPathVar.set(path)

    def browseFolder(var, title):
        path = filedialog.askdirectory(title=title, initialdir=var.get().strip() or scriptDir)
        if path:
            var.set(path)

    def browseNvdaAddon():
        path = filedialog.askopenfilename(
            title="Wybierz dodatek NVDA z glosem RHVoice",
            initialdir=workDirVar.get().strip() or scriptDir,
            filetypes=[("Dodatek NVDA", "*.nvda-addon"), ("Wszystkie pliki", "*.*")]
        )
        if not path:
            return
        nvdaAddonPathVar.set(path)
        speechSourceVar.set("nvda")
        try:
            info = inspectNvdaAddon(path)
            if (not voiceNameVar.get().strip()) or voiceNameVar.get().strip().lower() in ("polish", "voice"):
                voiceNameVar.set(info.get("name", "RHVoice"))
            setStatus("Wybrano dodatek RHVoice: " + info.get("name", "") + " " + info.get("language", ""))
        except Exception as err:
            setStatus("Dodatek NVDA nie jest obslugiwanym glosem RHVoice.")
            messagebox.showerror("Dodatek NVDA", str(err), parent=root)

    def refreshPorts():
        ports = []
        try:
            for port in serial.tools.list_ports.comports():
                label = port.device
                if port.description:
                    label += " - " + port.description
                ports.append((port.device, label))
                if not serialPortVar.get() and port.description.find("OpenGD77") == 0:
                    serialPortVar.set(port.device)
        except Exception as err:
            appendLog("Nie udało się odczytać portów COM: " + str(err))
        portsList.delete(0, "end")
        for device, label in ports:
            portsList.insert("end", label)
        if not serialPortVar.get() and ports:
            serialPortVar.set(ports[0][0])
        setStatus("Odświeżono listę portów. Wpisz port ręcznie albo wybierz go z listy.")

    def selectPortFromList(event=None):
        selection = portsList.curselection()
        if not selection:
            return
        item = portsList.get(selection[0])
        serialPortVar.set(item.split(" - ", 1)[0].strip())

    def checkDependencies():
        messages = []
        messages.append("Python: " + consolePythonExecutable())
        messages.append("tkinter: OK")
        try:
            import serial as serialModule
            messages.append("pyserial: OK (" + getattr(serialModule, "__version__", "wersja nieznana") + ")")
        except Exception as err:
            messages.append("pyserial: BŁĄD - " + str(err))

        ffmpegCandidate = ffmpegPathVar.get().strip()
        if ffmpegCandidate and os.path.exists(ffmpegCandidate):
            messages.append("ffmpeg: OK (" + ffmpegCandidate + ")")
        elif ffmpegAvailable():
            messages.append("ffmpeg: OK w PATH")
        else:
            messages.append("ffmpeg: BRAK. Wybierz ffmpeg.exe albo dodaj ffmpeg do PATH.")

        addonCandidate = nvdaAddonPathVar.get().strip()
        if addonCandidate:
            try:
                info = inspectNvdaAddon(addonCandidate)
                messages.append("NVDA/RHVoice add-on: OK (" + info.get("name", "unknown") + ")")
            except Exception as err:
                messages.append("NVDA/RHVoice add-on: ERROR - " + str(err))
        elif speechSourceVar.get() == "nvda":
            messages.append("NVDA/RHVoice add-on: missing .nvda-addon path.")

        if speechSourceVar.get() == "nvda" or addonCandidate or rhvoiceDllPathVar.get().strip():
            try:
                dll = findRhvoiceDll(rhvoiceDllPathVar.get().strip())
                messages.append("RHVoice.dll: OK (" + dll + ")")
            except Exception as err:
                messages.append("RHVoice.dll: ERROR - " + str(err))
        else:
            messages.append("RHVoice.dll: skipped because TTSMP3 is selected.")

        appendLog("Test zależności:")
        for message in messages:
            appendLog("  " + message)
        messagebox.showinfo("Test zależności", "\n".join(messages), parent=root)

    def buildCommand():
        args = []
        if modeVar.get() == "config":
            configPath = configPathVar.get().strip()
            if not configPath:
                raise ValueError("Wybierz plik konfiguracyjny CSV.")
            args.extend(["-c", configPath])
        else:
            wordlist = wordlistPathVar.get().strip()
            voiceName = voiceNameVar.get().strip()
            if not wordlist:
                raise ValueError("Wybierz plik wordlist CSV.")
            if not voiceName:
                raise ValueError("Podaj nazwę głosu lub folderu głosu.")
            if not (downloadVar.get() or encodeVar.get() or buildVar.get()):
                raise ValueError("Zaznacz przynajmniej jedną operację: pobieranie, kodowanie albo budowanie VPR.")
            args.extend(["-f", wordlist, "-n", voiceName])
            if serialPortVar.get().strip():
                args.extend(["-d", serialPortVar.get().strip()])
            if downloadVar.get():
                if speechSourceVar.get() == "nvda":
                    addonPath = nvdaAddonPathVar.get().strip()
                    if not addonPath:
                        raise ValueError("Wybierz plik .nvda-addon z glosem RHVoice.")
                    args.extend(["-N", addonPath])
                    if rhvoiceDllPathVar.get().strip():
                        args.extend(["-L", rhvoiceDllPathVar.get().strip()])
                else:
                    args.append("-T")
            if encodeVar.get():
                args.append("-e")
            if buildVar.get():
                outputPath = outputPathVar.get().strip()
                if not outputPath:
                    raise ValueError("Wybierz nazwę pliku wyjściowego VPR.")
                args.extend(["-b", outputPath])

        if overwriteVar.get():
            args.append("-o")
        if removeSilenceVar.get():
            args.append("-r")
        if gainVar.get().strip():
            args.extend(["-g", gainVar.get().strip()])
        if tempoVar.get().strip():
            args.extend(["-t", tempoVar.get().strip()])
        if aliasVar.get().strip():
            args.extend(["-A", aliasVar.get().strip()])
        return args

    def startRun():
        if currentProcess["proc"] is not None:
            messagebox.showwarning("Proces działa", "Builder już działa.", parent=root)
            return
        try:
            args = buildCommand()
            workDir = workDirVar.get().strip() or scriptDir
            if not os.path.isdir(workDir):
                raise ValueError("Folder roboczy nie istnieje: " + workDir)
        except Exception as err:
            messagebox.showerror("Brak danych", str(err), parent=root)
            setStatus(str(err))
            return

        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        env["PYTHONUNBUFFERED"] = "1"
        ffmpegCandidate = ffmpegPathVar.get().strip()
        if ffmpegCandidate and os.path.exists(ffmpegCandidate):
            env["PATH"] = os.path.dirname(ffmpegCandidate) + os.pathsep + env.get("PATH", "")
        if rhvoiceDllPathVar.get().strip():
            env["RHVOICE_DLL"] = rhvoiceDllPathVar.get().strip()

        if is_frozen_app():
            command = [sys.executable] + args
        else:
            command = [consolePythonExecutable(), "-u", scriptPath] + args
        appendLog("")
        appendLog("Start: " + " ".join(command))
        appendLog("Folder roboczy: " + workDir)
        setStatus("Builder działa. Log jest aktualizowany na bieżąco.")
        runButton.configure(state="disabled")
        stopButton.configure(state="normal")

        def worker():
            try:
                proc = subprocess.Popen(
                    command,
                    cwd=workDir,
                    env=env,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    bufsize=1,
                    creationflags=(CREATE_NO_WINDOW if os.name == "nt" else 0)
                )
                currentProcess["proc"] = proc
                for line in proc.stdout:
                    processQueue.put(("log", line.rstrip("\r\n")))
                code = proc.wait()
                processQueue.put(("done", code))
            except Exception as err:
                processQueue.put(("error", str(err)))

        threading.Thread(target=worker, daemon=True).start()

    def stopRun():
        proc = currentProcess["proc"]
        if proc is None:
            return
        appendLog("Zatrzymuję proces...")
        setStatus("Zatrzymywanie procesu.")
        try:
            proc.terminate()
        except Exception as err:
            appendLog("Nie udało się zatrzymać procesu: " + str(err))

    def pumpQueue():
        try:
            while True:
                kind, payload = processQueue.get_nowait()
                if kind == "log":
                    appendLog(payload)
                elif kind == "done":
                    currentProcess["proc"] = None
                    runButton.configure(state="normal")
                    stopButton.configure(state="disabled")
                    if payload == 0:
                        setStatus("Zakończono pomyślnie.")
                    else:
                        setStatus("Proces zakończył się błędem. Kod: " + str(payload))
                    appendLog("Koniec. Kod wyjścia: " + str(payload))
                elif kind == "error":
                    currentProcess["proc"] = None
                    runButton.configure(state="normal")
                    stopButton.configure(state="disabled")
                    setStatus("Błąd uruchamiania.")
                    appendLog("Błąd uruchamiania: " + payload)
        except queue.Empty:
            pass
        root.after(100, pumpQueue)

    def openWorkFolder():
        path = workDirVar.get().strip() or scriptDir
        if os.path.isdir(path):
            os.startfile(path)

    def clearLog():
        logText.configure(state="normal")
        logText.delete("1.0", "end")
        logText.configure(state="disabled")
        setStatus("Log wyczyszczony.")

    def refreshModeState():
        configMode = modeVar.get() == "config"
        configState = "normal" if configMode else "disabled"
        manualState = "disabled" if configMode else "normal"
        for widget in configWidgets:
            widget.configure(state=configState)
        for widget in manualWidgets:
            widget.configure(state=manualState)
        setStatus("Tryb: " + ("plik konfiguracyjny CSV" if configMode else "ręczny"))

    mainFrame = tk.Frame(root, padx=10, pady=8)
    mainFrame.pack(fill="both", expand=True)

    modeFrame = tk.LabelFrame(mainFrame, text="Tryb pracy")
    modeFrame.pack(fill="x")
    modeManual = tk.Radiobutton(modeFrame, text="Tryb ręczny", variable=modeVar, value="manual", command=refreshModeState)
    modeConfig = tk.Radiobutton(modeFrame, text="Plik konfiguracyjny CSV", variable=modeVar, value="config", command=refreshModeState)
    modeManual.grid(row=0, column=0, sticky="w", padx=6, pady=4)
    modeConfig.grid(row=0, column=1, sticky="w", padx=6, pady=4)
    describe(modeManual, "Tryb ręczny. Wybierasz wordlistę, głos, port i operacje.")
    describe(modeConfig, "Tryb pliku konfiguracyjnego CSV. Builder wykona operacje zapisane w CSV.")

    configFrame = tk.LabelFrame(mainFrame, text="Konfiguracja CSV")
    configFrame.pack(fill="x", pady=(8, 0))
    tk.Label(configFrame, text="Plik konfiguracyjny:").grid(row=0, column=0, sticky="w", padx=6, pady=4)
    configEntry = tk.Entry(configFrame, textvariable=configPathVar)
    configEntry.grid(row=0, column=1, sticky="ew", padx=6, pady=4)
    configBrowse = tk.Button(configFrame, text="Wybierz...", command=lambda: browseFile(configPathVar, "Wybierz plik konfiguracyjny", [("CSV", "*.csv"), ("Wszystkie pliki", "*.*")]))
    configBrowse.grid(row=0, column=2, padx=6, pady=4)
    configFrame.columnconfigure(1, weight=1)
    describe(configEntry, "Ścieżka do pliku konfiguracyjnego CSV.")

    manualFrame = tk.LabelFrame(mainFrame, text="Tryb ręczny")
    manualFrame.pack(fill="x", pady=(8, 0))
    tk.Label(manualFrame, text="Wordlist CSV:").grid(row=0, column=0, sticky="w", padx=6, pady=4)
    wordlistEntry = tk.Entry(manualFrame, textvariable=wordlistPathVar)
    wordlistEntry.grid(row=0, column=1, sticky="ew", padx=6, pady=4)
    wordlistBrowse = tk.Button(manualFrame, text="Wybierz...", command=lambda: browseFile(wordlistPathVar, "Wybierz wordlist CSV", [("CSV", "*.csv"), ("Wszystkie pliki", "*.*")]))
    wordlistBrowse.grid(row=0, column=2, padx=6, pady=4)

    tk.Label(manualFrame, text="Nazwa głosu/folder:").grid(row=1, column=0, sticky="w", padx=6, pady=4)
    voiceEntry = tk.Entry(manualFrame, textvariable=voiceNameVar)
    voiceEntry.grid(row=1, column=1, sticky="ew", padx=6, pady=4)

    tk.Label(manualFrame, text="Plik wyjściowy VPR:").grid(row=2, column=0, sticky="w", padx=6, pady=4)
    outputEntry = tk.Entry(manualFrame, textvariable=outputPathVar)
    outputEntry.grid(row=2, column=1, sticky="ew", padx=6, pady=4)
    outputBrowse = tk.Button(manualFrame, text="Wybierz...", command=browseOutput)
    outputBrowse.grid(row=2, column=2, padx=6, pady=4)

    tk.Label(manualFrame, text="Port COM radia:").grid(row=3, column=0, sticky="w", padx=6, pady=4)
    serialEntry = tk.Entry(manualFrame, textvariable=serialPortVar, width=16)
    serialEntry.grid(row=3, column=1, sticky="w", padx=6, pady=4)
    refreshPortsButton = tk.Button(manualFrame, text="Odśwież porty", command=refreshPorts)
    refreshPortsButton.grid(row=3, column=2, padx=6, pady=4)

    portsList = tk.Listbox(manualFrame, height=3, exportselection=False)
    portsList.grid(row=4, column=1, sticky="ew", padx=6, pady=4)
    portsList.bind("<<ListboxSelect>>", selectPortFromList)
    manualFrame.columnconfigure(1, weight=1)

    operationsFrame = tk.Frame(manualFrame)
    operationsFrame.grid(row=5, column=0, columnspan=3, sticky="w", padx=6, pady=4)
    downloadCheck = tk.Checkbutton(operationsFrame, text="Pobierz mowę z TTSMP3", variable=downloadVar)
    encodeCheck = tk.Checkbutton(operationsFrame, text="Koduj AMBE przez radio", variable=encodeVar)
    buildCheck = tk.Checkbutton(operationsFrame, text="Zbuduj plik VPR", variable=buildVar)
    downloadCheck.grid(row=0, column=0, sticky="w", padx=(0, 14))
    encodeCheck.grid(row=0, column=1, sticky="w", padx=(0, 14))
    buildCheck.grid(row=0, column=2, sticky="w")

    speechFrame = tk.LabelFrame(mainFrame, text="Zrodlo mowy")
    speechFrame.pack(fill="x", pady=(8, 0))
    speechTtsRadio = tk.Radiobutton(speechFrame, text="TTSMP3", variable=speechSourceVar, value="ttsmp3")
    speechNvdaRadio = tk.Radiobutton(speechFrame, text="Dodatek NVDA/RHVoice", variable=speechSourceVar, value="nvda")
    speechTtsRadio.grid(row=0, column=0, sticky="w", padx=6, pady=4)
    speechNvdaRadio.grid(row=0, column=1, sticky="w", padx=6, pady=4)
    tk.Label(speechFrame, text="Plik .nvda-addon:").grid(row=1, column=0, sticky="w", padx=6, pady=4)
    nvdaAddonEntry = tk.Entry(speechFrame, textvariable=nvdaAddonPathVar)
    nvdaAddonEntry.grid(row=1, column=1, sticky="ew", padx=6, pady=4)
    nvdaAddonBrowse = tk.Button(speechFrame, text="Wybierz...", command=browseNvdaAddon)
    nvdaAddonBrowse.grid(row=1, column=2, padx=6, pady=4)
    tk.Label(speechFrame, text="RHVoice.dll:").grid(row=2, column=0, sticky="w", padx=6, pady=4)
    rhvoiceDllEntry = tk.Entry(speechFrame, textvariable=rhvoiceDllPathVar)
    rhvoiceDllEntry.grid(row=2, column=1, sticky="ew", padx=6, pady=4)
    rhvoiceDllBrowse = tk.Button(speechFrame, text="Wybierz...", command=lambda: browseFile(rhvoiceDllPathVar, "Wybierz RHVoice.dll", [("RHVoice.dll", "RHVoice.dll"), ("DLL", "*.dll"), ("Wszystkie pliki", "*.*")]))
    rhvoiceDllBrowse.grid(row=2, column=2, padx=6, pady=4)
    speechFrame.columnconfigure(1, weight=1)

    optionsFrame = tk.LabelFrame(mainFrame, text="Opcje")
    optionsFrame.pack(fill="x", pady=(8, 0))
    tk.Label(optionsFrame, text="Folder roboczy:").grid(row=0, column=0, sticky="w", padx=6, pady=4)
    workDirEntry = tk.Entry(optionsFrame, textvariable=workDirVar)
    workDirEntry.grid(row=0, column=1, sticky="ew", padx=6, pady=4)
    workDirBrowse = tk.Button(optionsFrame, text="Wybierz...", command=lambda: browseFolder(workDirVar, "Wybierz folder roboczy"))
    workDirBrowse.grid(row=0, column=2, padx=6, pady=4)

    tk.Label(optionsFrame, text="ffmpeg.exe:").grid(row=1, column=0, sticky="w", padx=6, pady=4)
    ffmpegEntry = tk.Entry(optionsFrame, textvariable=ffmpegPathVar)
    ffmpegEntry.grid(row=1, column=1, sticky="ew", padx=6, pady=4)
    ffmpegBrowse = tk.Button(optionsFrame, text="Wybierz...", command=lambda: browseFile(ffmpegPathVar, "Wybierz ffmpeg.exe", [("ffmpeg.exe", "ffmpeg.exe"), ("EXE", "*.exe"), ("Wszystkie pliki", "*.*")]))
    ffmpegBrowse.grid(row=1, column=2, padx=6, pady=4)

    tk.Label(optionsFrame, text="Głośność dB:").grid(row=2, column=0, sticky="w", padx=6, pady=4)
    gainEntry = tk.Entry(optionsFrame, textvariable=gainVar, width=8)
    gainEntry.grid(row=2, column=1, sticky="w", padx=6, pady=4)
    tk.Label(optionsFrame, text="Tempo:").grid(row=2, column=1, sticky="w", padx=(95, 6), pady=4)
    tempoEntry = tk.Entry(optionsFrame, textvariable=tempoVar, width=8)
    tempoEntry.grid(row=2, column=1, sticky="w", padx=(150, 6), pady=4)
    tk.Label(optionsFrame, text="Alias tempa:").grid(row=2, column=1, sticky="w", padx=(235, 6), pady=4)
    aliasEntry = tk.Entry(optionsFrame, textvariable=aliasVar, width=14)
    aliasEntry.grid(row=2, column=1, sticky="w", padx=(320, 6), pady=4)

    overwriteCheck = tk.Checkbutton(optionsFrame, text="Nadpisuj istniejące pliki", variable=overwriteVar)
    removeSilenceCheck = tk.Checkbutton(optionsFrame, text="Usuń ciszę z początku", variable=removeSilenceVar)
    overwriteCheck.grid(row=3, column=0, sticky="w", padx=6, pady=4)
    removeSilenceCheck.grid(row=3, column=1, sticky="w", padx=6, pady=4)
    optionsFrame.columnconfigure(1, weight=1)

    buttonsFrame = tk.Frame(mainFrame)
    buttonsFrame.pack(fill="x", pady=(8, 0))
    runButton = tk.Button(buttonsFrame, text="Uruchom Alt+R", command=startRun)
    stopButton = tk.Button(buttonsFrame, text="Zatrzymaj Alt+S", command=stopRun, state="disabled")
    depsButton = tk.Button(buttonsFrame, text="Test zależności", command=checkDependencies)
    openButton = tk.Button(buttonsFrame, text="Otwórz folder", command=openWorkFolder)
    clearButton = tk.Button(buttonsFrame, text="Wyczyść log", command=clearLog)
    closeButton = tk.Button(buttonsFrame, text="Zamknij", command=root.destroy)
    for idx, button in enumerate([runButton, stopButton, depsButton, openButton, clearButton, closeButton]):
        button.grid(row=0, column=idx, padx=4, pady=4, sticky="w")

    statusFrame = tk.LabelFrame(mainFrame, text="Status i log")
    statusFrame.pack(fill="both", expand=True, pady=(8, 0))
    tk.Label(statusFrame, textvariable=statusVar, anchor="w").pack(fill="x", padx=6, pady=(4, 2))
    logFrame = tk.Frame(statusFrame)
    logFrame.pack(fill="both", expand=True, padx=6, pady=4)
    logScroll = tk.Scrollbar(logFrame)
    logScroll.pack(side="right", fill="y")
    logText = tk.Text(logFrame, wrap="word", height=12, yscrollcommand=logScroll.set)
    logText.pack(side="left", fill="both", expand=True)
    logScroll.configure(command=logText.yview)
    logText.configure(state="disabled")

    configWidgets = [configEntry, configBrowse]
    manualWidgets = [
        wordlistEntry, wordlistBrowse, voiceEntry, outputEntry, outputBrowse,
        serialEntry, refreshPortsButton, portsList, downloadCheck, encodeCheck, buildCheck,
        speechTtsRadio, speechNvdaRadio, nvdaAddonEntry, nvdaAddonBrowse, rhvoiceDllEntry, rhvoiceDllBrowse
    ]

    for widget, text in [
        (configEntry, "Plik konfiguracyjny CSV."),
        (wordlistEntry, "Plik CSV z kolumnami promptów."),
        (voiceEntry, "Nazwa głosu i folderu na pliki audio."),
        (outputEntry, "Bazowa nazwa pliku VPR. Program utworzy warianty UV380-like i monochrome."),
        (serialEntry, "Port COM radia OpenGD77, na przykład COM5."),
        (portsList, "Lista wykrytych portów. Strzałkami wybierz port."),
        (workDirEntry, "Folder roboczy dla plików tymczasowych i ścieżek względnych."),
        (ffmpegEntry, "Ścieżka do ffmpeg.exe albo puste, jeśli ffmpeg jest w PATH."),
        (speechTtsRadio, "Zrodlo mowy: internetowa usluga TTSMP3."),
        (speechNvdaRadio, "Zrodlo mowy: lokalny glos RHVoice z dodatku NVDA."),
        (nvdaAddonEntry, "Plik .nvda-addon zawierajacy glos RHVoice."),
        (rhvoiceDllEntry, "Opcjonalna sciezka do RHVoice.dll. Puste oznacza automatyczne wykrywanie."),
        (gainEntry, "Zmiana głośności w decybelach."),
        (tempoEntry, "Tempo audio od 0.5 do 2."),
        (aliasEntry, "Opcjonalny alias tempa używany w nazwie pliku."),
        (logText, "Log działania buildera.")
    ]:
        describe(widget, text)

    root.bind_all("<Alt-r>", lambda event: startRun())
    root.bind_all("<Alt-s>", lambda event: stopRun())
    root.bind_all("<Alt-l>", lambda event: logText.focus_set())
    root.bind_all("<F5>", lambda event: refreshPorts())

    refreshPorts()
    refreshModeState()
    root.after(100, pumpQueue)
    wordlistEntry.focus_set()
    root.mainloop()
    return 0

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        sys.exit(run_accessible_gui())
    sys.exit(main() or 0)
