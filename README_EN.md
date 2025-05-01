## Requirements Document

#### Project Name:

​						Mouse Locator XYSpy

#### EXE Program Usage Instructions:

This project has been packaged into a standalone executable program (.exe) for the Windows platform using PyInstaller. It runs without requiring a separate Python environment.

<img src="img/README.assets/image-20250501230503783.png" alt="image-20250501230503783" style="zoom:67%;" />

##### Usage Steps:

1. Download the `XYSpy.exe` file (available on the release page).
2. Double-click to launch the graphical interface—no installation required.
3. Once running, the program will reside in the system tray. Press the Alt key to record the current mouse position, which will automatically be copied to the clipboard.
4. Click the “Move to Position” button to move the mouse to the last recorded coordinates.
5. To exit the program, right-click the tray icon and select “Exit.”

##### Notes:

If Windows Defender SmartScreen blocks the startup, choose “Run Anyway.”

If the program is unresponsive or fails to capture key events in certain windows, try running it as administrator.

The program is compressed using UPX; some antivirus software may falsely report it as suspicious.

##### System Requirements:

Supported OS: Windows 10 or higher.

------

#### Project Goals:

- Provide a simple and efficient tool to help users record and locate mouse positions.
- Offer a lightweight and user-friendly graphical interface.

#### Project Description:

Mouse Locator XYSpy is a lightweight mouse tracking tool that allows users to press the `Alt` key to record the current mouse position, which is then copied to the clipboard. Users can click the “Move to Position” button to return the mouse to the last recorded coordinates. The tool aims to simplify the process of mouse coordinate logging and positioning.

#### Technology Stack:

- **Python**: Primary programming language
- **CustomTkinter**: GUI framework for cross-platform interfaces
- **PyAutoGUI**: Used to obtain and control mouse position
- **Pyperclip**: Used to copy coordinates to clipboard
- **Keyboard**: Used to detect keyboard events
- **pystray**: Used to create system tray icons
- **Pillow**: Used to load and display tray icons
- **locale**: Used to detect system language environment

#### Project Structure:

```
bash复制编辑XYSpy/
│
├── images/                       # Icons and other resources
│   └── xy_logo_com.ico           # Application icon
│
├── XYSpy.py                      # Main entry point and logic
│
└── README.md                     # Project documentation
```

#### Functional Requirements:

1. **User Interface**:
   - Display the current mouse position.
   - Provide a “Clear” button to reset the text box.
   - Provide a “Move to Position” button to move the mouse to the last recorded location.
   - Provide a “Help” button to show usage instructions.
2. **Mouse Position Logging**:
   - When the `Alt` key is pressed, automatically log the current mouse position and copy it to the clipboard.
   - Format of logged coordinates: `(x, y)` and display in the text box.
3. **Move to Position**:
   - When the user clicks the “Move to Position” button, the mouse should move to the last saved coordinates.
4. **Tray Icon**:
   - Show an icon in the system tray with a right-click menu that includes an “Exit” option.
5. **Multilingual Support**:
   - Automatically detect system language and display the interface in either English or Chinese.

#### System Requirements:

- **Operating System**: Windows
- **Python Version**: 3.7 or later
- **Required Libraries**:
  - customtkinter
  - keyboard
  - pyautogui
  - pyperclip
  - pystray
  - Pillow
  - locale

#### Installation Guide:

1. Install Python 3.7 or later.

2. Clone the project locally:

   ```bash
   git clone https://github.com/your-username/XYSpy.git
   ```

3. Install required Python libraries:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the program:

   ```bash
   python XYSpy.py
   ```

#### Packaging Instructions:

The program is packaged using **PyInstaller** and compressed with **UPX**. Below is the packaging command:

```bash
pyinstaller --upx-dir=D:\Tool\upx-5.0.0-win64\upx.exe -w --onefile --add-data "images;images" --icon=images\xy_logo_com.ico --manifest admin.manifest --clean XYSpy.py
```

- `--upx-dir`: Path to the UPX tool (optional)
- `-w` or `--windowed`: Hides the console window
- `--onefile`: Package as a single executable
- `--add-data`: Include resource files (e.g., icons)
- `--icon`: Set application icon
- `--manifest`: Use EXE manifest to request administrator privileges (optional)
- `--clean`: Clean previous build caches

#### Exit Instructions:

Right-click the tray icon and select “Exit” to close the program.

#### Error Handling:

- If an invalid coordinate format is detected, the system will show a “Format Invalid” message.
- If mouse movement fails, the system will display “Move Failed” along with the error message.

#### Language Support:

- Supports Chinese and English. Automatically switches based on system locale.

#### TODO:

- Add support for other operating systems (macOS, Linux).
- Add settings UI for custom hotkeys, themes, etc.

> No further updates are expected.

#### Version History:

- **v1.0.0** (2025-05-01) - Initial Release
  - Mouse position logging, movement, and text clearing.
  - Tray icon and right-click exit menu.
  - Multilingual support: Chinese and English.
  - Packaged as a standalone executable using PyInstaller.

#### License:

This project is licensed under the **MIT License**. You are free to use, modify, and distribute the code as long as the original license and copyright notice are included.

See MIT License for full details.

#### Disclaimer:

This project and its code are provided “as is,” without any warranties. The author is not liable for any direct or indirect damages arising from the use of this software.