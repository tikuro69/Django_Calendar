import json
from .models import Event
from .forms import EventForm
from django.http import Http404
import time
import zoneinfo

from django.template import loader
from django.http import HttpResponse
from django.middleware.csrf import get_token
from django.http import JsonResponse
from .forms import CalendarForm

from django.utils.timezone import make_aware

from datetime import datetime, timezone, timedelta
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect


# Create your views here.

def index(request):
    """
    カレンダー画面
    """
    # CSRFのトークンを発行する
    get_token(request)
    template = loader.get_template("sc/index.html")
    return HttpResponse(template.render())


def add_event(request):
    """
    イベント登録
    """

    if request.method == "GET":
        # GETは対応しない
        raise Http404()

    # JSONの解析
    datas = json.loads(request.body)

    # バリデーション
    eventForm = EventForm(datas)
    if eventForm.is_valid() == False:
        # バリデーションエラー
        raise Http404()

    # リクエストの取得
    start_date = datas["start_date"]
    end_date = datas["end_date"]
    event_name = datas["event_name"]

    # 日付に変換。タイムスタンプはミリ秒なので秒に変換しawareに　
    st = time.localtime(start_date / 1000)
    et = time.localtime(end_date / 1000)
    start_filter = datetime(st.tm_year, st.tm_mon,
                            st.tm_mday, tzinfo=zoneinfo.ZoneInfo('Asia/Tokyo'))
    end_filter = datetime(et.tm_year, et.tm_mon, et.tm_mday,
                          tzinfo=zoneinfo.ZoneInfo('Asia/Tokyo'))
    # 登録処理
    event = Event(
        event_name=str(event_name),
        start=start_filter,
        end=end_filter,
    )
    event.save()

    # 登録情報を返却用リストに追加
    res = []
    res.append(
        {
            'id': event.id,
            "title": event.event_name,
            "start": event.start,
            "end": event.end,
            "textColor": 'black',
            "backgroundColor": "#AFDFE4",
        }
    )

    # リストを返却
    return JsonResponse(res, safe=False)


def get_events(request):
    """
    イベントの取得
    """

    if request.method == "GET":
        # GETは対応しない
        raise Http404()

    # JSONの解析
    datas = json.loads(request.body)
    # バリデーション
    calendarForm = CalendarForm(datas)
    if calendarForm.is_valid() == False:
        # バリデーションエラー
        raise Http404()

    # リクエストの取得
    start_date = datas["start_date"]
    end_date = datas["end_date"]

    # 日付に変換。タイムスタンプはミリ秒なので秒に変換しawareに　
    st = time.localtime(start_date / 1000)
    et = time.localtime(end_date / 1000)
    start_filter = datetime(st.tm_year, st.tm_mon,
                            st.tm_mday, tzinfo=zoneinfo.ZoneInfo('Asia/Tokyo'))
    end_filter = datetime(et.tm_year, et.tm_mon, et.tm_mday,
                          tzinfo=zoneinfo.ZoneInfo('Asia/Tokyo'))

    # FullCalendarの表示範囲のみ表示
    events = Event.objects.filter(
        start__lt=end_filter, end__gt=start_filter
    )

    # fullcalendarのため配列で返却
    list = []
    for event in events:
        list.append(
            {
                'id': event.id,
                "title": event.event_name,
                "start": event.start,
                "end": event.end,
                "textColor": 'black',
                "backgroundColor": "#AFDFE4",
            }
        )

    return JsonResponse(list, safe=False)


def remove_event(request):
    """
    イベントの削除
    """

    if request.method == "GET":
        # GETは対応しない
        raise Http404()

    events = json.loads(request.body)
    # リクエストの取得
    event_id = events["event_id"]
    event = Event.objects.get(id=event_id)
    event.delete()
    return HttpResponse("")


def drop_event(request):
    """
    イベントドロップ処理
    """

    if request.method == "GET":
        # GETは対応しない
        raise Http404()

    events = json.loads(request.body)
    # リクエストの取得

    event_id = events["event_id"]
    delta = events["event_delta"]
    event = Event.objects.get(id=event_id)

    # ドロップ元にドロップ先との差分処理
    event.start = event.start + \
        timedelta(days=delta["days"]) + \
        timedelta(milliseconds=delta["milliseconds"])
    event.end = event.end + \
        timedelta(days=delta["days"]) + \
        timedelta(milliseconds=delta["milliseconds"])

    event.save()
    return HttpResponse("")


def resize_event(request):
    """
    リサイズ処理(終了点のみリサイズ)
    """

    if request.method == "GET":
        # GETは対応しない
        raise Http404()

    events = json.loads(request.body)
    # リクエストの取得
    event_id = events["event_id"]
    end = events["event_end"]

    # end_timeをリサイズ値に変更
    event = Event.objects.get(id=event_id)
    event.end = end

    event.save()
    return HttpResponse("")
