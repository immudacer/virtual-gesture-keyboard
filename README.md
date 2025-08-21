# 🖐️ Virtual Gesture Keyboard

A **gesture-controlled virtual keyboard** built with **OpenCV, CVZone, and PyAutoGUI**.
This project allows you to type on any application using **hand gestures captured from your webcam**.

It supports:

* ✅ Lowercase letters
* ✅ Uppercase letters (Shift)
* ✅ Symbols and numbers
* ✅ Special keys: **Space** & **Backspace**
* ✅ Multiple layouts (lowercase / uppercase / symbols)



## 🚀 Features

* **Hand-tracking with CVZone**
* **Finger pinch gesture** for pressing keys
* Smooth **virtual keyboard UI with gradients and shadows**
* Works on **Windows, Linux, and macOS**
* Can type into **any active application** (Notepad, Browser, VS Code, etc.)



## 📦 Requirements

Make sure you have **Python 3.8+** installed.
Install dependencies with:

```bash
pip install opencv-python cvzone pyautogui numpy
```


## ⚙️ How to Run

1. **Clone this repository**

   ```bash
   git clone https://github.com/immudacer/virtual-gesture-keyboard.git
   cd virtual-gesture-keyboard
   ```

2. **Run the script**

   ```bash
   python main.py
   ```

3. **Controls**

   * Point your index finger at a key → Highlight
   * Bring **index + thumb together (pinch)** → Press the key
   * **aA / Aa** → Switch lowercase / uppercase
   * **\$/** → Switch to symbols
   * **ab** → Switch back to lowercase
   * **SPACE** → Insert space
   * **\<x** → Backspace

4. To exit the app → Press **`q`** on your keyboard


## 💻 Supported Operating Systems

* **Windows** 🟦

  * Works directly with webcam
  * PyAutoGUI handles key events for all applications
* **Linux** 🐧

  * Works with X11 (default desktop environments)
  * Some Wayland sessions may need tweaks (recommend running on X11)
* **macOS** 🍎

  * Works, but you may need to give **Accessibility Permissions** to Python in **System Preferences → Security & Privacy → Accessibility**



## 🔧 Notes

* For **best performance**, make sure your **webcam resolution** is at least **720p**
* If keys feel too small/large, tweak the values in `create_buttons()` function
* Works in **real-time** (\~30 FPS depending on your camera & system)



## 🤝 Contributing

Pull requests are welcome. Feel free to fork the repo and add new layouts, themes, or gestures.



## 📜 License

MIT License – free to use & modify.


