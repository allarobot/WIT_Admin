
    $("#btn-chat").on("click", function() {
            htmlNote = $("#note_record").html();
            var input_msg = $("#btn-input").val()
            var datetime = (new Date()).toLocaleString();
            var user = "jay"
            console.log(input_msg)
            //替换相关的字段值
            htmlNote = del_html_tags(htmlNote, "str_user", user);                  //修改User
            htmlNote = del_html_tags(htmlNote, "str_note", input_msg);        //添加Note
            htmlNote = del_html_tags(htmlNote, "str_datetime", datetime);
            $(".chat").append(htmlNote);                                //替换之后追加chat list
            $("#btn-input").val("")

    })
    //自定义一个方法批量替换制定的字符
    function del_html_tags(str, reallyDo, replaceWith) {
        var e = new RegExp(reallyDo, "g");
        words = str.replace(e, replaceWith);
        return words;
    }

