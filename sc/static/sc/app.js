// CSRF対策
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
axios.defaults.xsrfCookieName = "csrftoken"

document.addEventListener('DOMContentLoaded', function () {

    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        // themeSystem: 'bootstrap',
        locale: 'ja',
        initialView: 'dayGridMonth',
        headerToolbar: {
            left: 'title',
            center: 'dayGridMonth,timeGridWeek,timeGridDay,listMonth',
            right: 'prev,today,next'
        },
        editable: true,
        // 日付をクリック、または範囲を選択したイベント
        selectable: true,

        // 日付をセレクト
        select: function (info) {
            if (window.confirm("selected " + info.startStr + " to " + info.endStr)) {
            // 入力ダイアログ
            const eventName = prompt("イベントを入力してください");         
            if (eventName) {
                // 登録処理の呼び出し
                axios
                    .post("/add/", {
                        start_date: info.start.valueOf(),
                        end_date: info.end.valueOf(),
                        event_name: eventName,
                    })
                    .then((response) => {
                        // イベントの追加
                        console.log(response.data);
                        console.log(response.data[0].id);
                        calendar.addEvent({
                            id: response.data[0].id,
                            title: eventName,
                            start: info.start,
                            end: info.end,
                            AllDay: true,
                            backgroundColor: response.data[0].backgroundColor,
                            textColor: 'black',
                        });
                    })
                    .catch(() => {
                        // バリデーションエラー
                        alert("登録に失敗しました");
                    });
            }
            }
        },
        
        // イベントの表示
        events: function (info, successCallback, failureCallback) {

            axios
                .post("/list/", {
                    start_date: info.start.valueOf(),
                    end_date: info.end.valueOf(),
                })
                .then((response) => {
                    calendar.removeAllEvents();
                    successCallback(response.data);
                })
                .catch(() => {
                    // バリデーションエラー
                    alert("登録に失敗しました");
                });
        },
        
        // イベントクリックで削除
        eventClick: function(info) {
            const removeEvent = window.confirm('予定を削除しますか？' + info.event.title);

            if (removeEvent) {
                axios
                .post("/remove/", {
                    event_id: info.event.id,
                })
                .then(() => {
                    info.event.remove();
                })
                .catch(() => {
                    alert("登録に失敗しました");
                })
                };
        },

        // ドラック＆ドロップで変更
        eventDrop: function(info) {
            alert(info.event.title + " was drop on " + info.event.start);

                axios
                .post("/move/", {
                    event_id: info.event.id,
                    event_delta: info.delta,
                })
                .then(() => {
                    console.log("成功しました")
                })
                .catch(() => {
                    info.revert();
                    alert("登録に失敗しました");
                });

        },

        // 下側ドラックでリサイズ
        eventResize: function(info) {
            alert(info.event.title + " was resize on " + info.event.end);

                axios
                .post("/resize/", {
                    event_id: info.event.id,
                    event_start: info.event.start,
                    event_end: info.event.end,

                })
                .then(() => {
                    console.log("成功しました")
                })
                .catch(() => {
                    info.revert();
                    alert("登録に失敗しました");
                });

        },

    });

    calendar.render();
});


