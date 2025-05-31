import sys
import ctypes

from verble import VerbleApp

def maximize_console_window():
        if sys.platform.startswith("win"):
            user32 = ctypes.WinDLL('user32')
            if user32:
                h_wnd = user32.GetForegroundWindow()           
                if h_wnd:
                    user32.ShowWindow(h_wnd, 3)
        else:
            print("\033[9;1t", end="", flush=True)

if __name__ == "__main__":
    maximize_console_window()
    VerbleApp().run()