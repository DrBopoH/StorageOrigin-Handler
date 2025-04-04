from typing import List
import pytest, os

json_examples: List = [
	{
		"widget": {
			"debug": "on",
			"window": {
				"title": "Sample Konfabulator Widget",
				"name": "main_window",
				"width": 500,
				"height": 500
			},
			"image": { 
				"src": "Images/Sun.png",
				"name": "sun1",
				"hOffset": 250,
				"vOffset": 250,
				"alignment": "center"
			},
			"text": {
				"data": "Click Here",
				"size": 36,
				"style": "bold",
				"name": "text1",
				"hOffset": 250,
				"vOffset": 100,
				"alignment": "center",
				"onMouseUp": "sun1.opacity = (sun1.opacity / 100) * 90;"
			}
		}
	},
	{
		"menu": {
			"header": "SVG Viewer",
			"items": [
				{"id": "Open"},
				{"id": "OpenNew", "label": "Open New"},
				{"id": "ZoomIn", "label": "Zoom In"},
				{"id": "ZoomOut", "label": "Zoom Out"},
				{"id": "OriginalView", "label": "Original View"},
				{"id": "Quality"},
				{"id": "Pause"},
				{"id": "Mute"},
				{"id": "Find", "label": "Find..."},
				{"id": "FindAgain", "label": "Find Again"},
				{"id": "Copy"},
				{"id": "CopyAgain", "label": "Copy Again"},
				{"id": "CopySVG", "label": "Copy SVG"},
				{"id": "ViewSVG", "label": "View SVG"},
				{"id": "ViewSource", "label": "View Source"},
				{"id": "SaveAs", "label": "Save As"},
				{"id": "Help"},
				{"id": "About", "label": "About Adobe CVG Viewer..."}
			]
		}
	},
	{
		"id":1,
		"age": 17,
		"username":"ivan",
		"email":"ivan777@gmail.com",
		"timecreated": "2024-03-22 12:00:00",
		"posts": {
			"my dog": {
				"id": 197,
				"content": "_vvv DOG vvv_",
				"timecreated": "2025-01-05 19:45:00"
			}
		}
	}
]



