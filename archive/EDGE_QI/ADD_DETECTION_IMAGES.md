# 📸 How to Add Your Detection Images to Live Feeds

## Quick Steps

Your YOLO detection images need to be copied to the frontend public folder so they display in the live camera feeds.

### 1. Copy Your Detection Images

Copy these 4 images from your models folder to the frontend:

```powershell
# From PowerShell in your project root:

# Image 1 - Downtown Intersection (0000280_01401_d_0000619.jpg)
Copy-Item "d:\EDGE_QI_!\EDGE_QI\models\evaluation\yolov8n_validation_20251101_194104\predictions\0000280_01401_d_0000619.jpg" `
  -Destination "d:\EDGE_QI_!\EDGE_QI\frontend\public\detections\camera_1_street_view.jpg"

# Image 2 - Highway 101 (0000199_01269_d_0000166.jpg)
Copy-Item "d:\EDGE_QI_!\EDGE_QI\models\evaluation\yolov8n_validation_20251101_194104\predictions\0000199_01269_d_0000166.jpg" `
  -Destination "d:\EDGE_QI_!\EDGE_QI\frontend\public\detections\camera_2_highway.jpg"

# Image 3 - Residential Parking (0000026_03000_d_0000030.jpg)
Copy-Item "d:\EDGE_QI_!\EDGE_QI\models\evaluation\yolov8n_validation_20251101_194104\predictions\0000026_03000_d_0000030.jpg" `
  -Destination "d:\EDGE_QI_!\EDGE_QI\frontend\public\detections\camera_3_parking.jpg"

# Image 4 - Commercial Plaza (0000287_00601_d_0000762.jpg)
Copy-Item "d:\EDGE_QI_!\EDGE_QI\models\evaluation\yolov8n_validation_20251101_194104\predictions\0000287_00601_d_0000762.jpg" `
  -Destination "d:\EDGE_QI_!\EDGE_QI\frontend\public\detections\camera_4_plaza.jpg"
```

### 2. If Images Are in Different Location

If your images are saved elsewhere, find them and copy to:
- `d:\EDGE_QI_!\EDGE_QI\frontend\public\detections\`

Name them:
- `camera_1_street_view.jpg` - Downtown intersection with many cars
- `camera_2_highway.jpg` - Highway with bus and trucks  
- `camera_3_parking.jpg` - Parking lot bird's eye view
- `camera_4_plaza.jpg` - Commercial area with people

### 3. Verify Images Are There

```powershell
Get-ChildItem "d:\EDGE_QI_!\EDGE_QI\frontend\public\detections\"
```

You should see 4 .jpg files.

### 4. Refresh Browser

Once images are copied:
1. Go to http://localhost:5173
2. Click "Live Cameras" 
3. You should see your actual YOLO detection images!

---

## Image Mapping

| Camera | Backend Path | Display Name | Expected Image |
|--------|-------------|--------------|----------------|
| Node 1 | `/detections/camera_1_street_view.jpg` | Downtown Intersection | 16+ cars, 1 pedestrian |
| Node 2 | `/detections/camera_2_highway.jpg` | Highway 101 | Cars, bus, truck |
| Node 3 | `/detections/camera_3_parking.jpg` | Residential Parking | Cars, van, tricycle |
| Node 4 | `/detections/camera_4_plaza.jpg` | Commercial Plaza | Cars, people |
| Node 5 | `/detections/camera_5_school.jpg` | School Zone | (placeholder) |

---

## Alternative: Use Your Attachments

Since you attached the images in the chat, you can also:

1. **Save the attachments** from your chat to your computer
2. **Rename them** to match the camera names:
   - `camera_1_street_view.jpg`
   - `camera_2_highway.jpg`
   - `camera_3_parking.jpg`
   - `camera_4_plaza.jpg`
3. **Copy to** `d:\EDGE_QI_!\EDGE_QI\frontend\public\detections\`
4. **Refresh** the browser

---

## Current Status

✅ Black UI theme applied
✅ Live camera feed components ready
✅ Backend serving from `/detections/` path
✅ 45 detection records with exact coordinates
✅ All 5 nodes configured

⏳ **Waiting for**: Image files to be copied to `frontend/public/detections/`

Once images are there, they will automatically appear in the live feeds!

---

## Troubleshooting

**Images still not showing?**

1. Check browser console (F12) for 404 errors
2. Verify files are in correct location
3. Check file names match exactly (case-sensitive on some systems)
4. Make sure backend is serving static files (already configured)
5. Hard refresh browser (Ctrl+Shift+R)

**Where are my original images?**

Try searching:
```powershell
Get-ChildItem -Path "d:\EDGE_QI_!\EDGE_QI\" -Recurse -Filter "0000280_01401_d_0000619.jpg"
```
