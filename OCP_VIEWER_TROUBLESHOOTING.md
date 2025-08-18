# OCP Viewer Troubleshooting Guide

## ✅ Fixed Issues
- **Port Detection Error**: Fixed by explicitly setting `set_port(3939)` 
- **Package Installation**: noah123d is now properly installed
- **Data Transfer**: Scripts are successfully sending data to viewer (165KB+ payloads)

## 🔍 Current Status
- WebSocket connections are working (127.0.0.1:3939)
- ocp-vscode version: 2.9.0 (upgraded from 2.7.1)
- ColorMapHelper is working correctly
- Data is being sent to viewer successfully

## 🛠️ If You Still Can't See Objects

### 1. Open OCP Viewer Panel
- In VS Code, go to **View > Command Palette** (Cmd+Shift+P)
- Type "OCP" and look for "OCP: Show Viewer" or similar command
- Or look for an OCP viewer tab/panel in VS Code

### 2. Camera/Zoom Issues
The objects might be there but not visible due to camera position:
- **Zoom out**: Use mouse wheel to zoom out significantly
- **Reset view**: Look for a "Reset Camera" or "Fit All" button in the viewer
- **Pan around**: Click and drag to pan the view

### 3. Object Size Issues
- Objects might be very small or very large
- Try zooming way out or way in
- The spheres in our example are size 1.0 with spacing 2.0

### 4. Browser/Viewer Issues
- Try refreshing the OCP viewer panel
- Close and reopen the viewer
- Restart VS Code if necessary

### 5. Test with Simple Object
Run this simple test:
```python
from build123d import Box
from ocp_vscode import show, set_port

set_port(3939)
box = Box(10, 10, 10)  # Large box
show(box)
```

### 6. Extension Issues
- Make sure the OCP viewer extension is installed and enabled
- Check VS Code extensions panel for OCP-related extensions
- Extension might need to be reloaded

## 🔧 Debug Information
- Port: 3939 (working)
- WebSocket connections: ✅ Successful  
- Data transfer: ✅ Large payloads being sent
- Script execution: ✅ No errors
- ColorMapHelper: ✅ All methods working

The technical connection is working perfectly. The issue is likely with the viewer display or camera position.
