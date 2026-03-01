# -*- coding: utf-8 -*-
"""
游戏 API 端点
"""
from fastapi import APIRouter
from fastapi.responses import FileResponse
import os

router = APIRouter(tags=["游戏"])


@router.get("/game", summary="飞机大战游戏")
def game_page():
    """飞机大战游戏页面"""
    game_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "static", "game.html")
    return FileResponse(game_path, media_type="text/html")
