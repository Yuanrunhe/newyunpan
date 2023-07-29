const form = document.getElementById("my-form");
const formContainer = $("#form-container");

// 点击上传按钮事件
function add_btn() {
    $(".btn-add").click(function () {
        $.ajax({
            url: "/yunpan/add_folder/",
            type: "GET",
            dataType: "html",
            success: function (response) {
                formContainer.html(response);
                $(".add_modal").modal('show');
            },
            error: function (xhr, status, error) {
                console.log(error);
            }
        });
    });
}

function create_folder() {
    $(".create-folder").click(function () {
        const inputValue = $('.file-name-input').val();
        if (inputValue === '') {
            alert('请输入正确文件名');
        } else {
            const btnId = $('.btn_sc').attr('id');
            const ccID = sessionStorage.getItem('ccID');
            $.ajax({
                url: "/yunpan/api/creatfolder/",
                type: 'POST',
                data: {"btnId": btnId, "inputValue": inputValue, "ccID": ccID},
                dataType: 'json',
                success: function (response) {
                    if (response.success) {
                        console.log("创建成功")
                        $("#create_f").hide();
                        window.location.reload();
                    } else {
                        console.log("创建失败")
                    }
                }
            });
        }
    })
}

// 上传文件文件确认按钮
function tj_btn() {
    $(".sub_folder").click(function () {
        // 获取上传的文件
        const formData = new FormData($("#my-form")[0]);

        // 获取上传的文件夹名称
        const folderInput = $('#id_directory');
        const folderPath = folderInput[0].files[0].webkitRelativePath;
        const folderName = folderPath.split('/')[0];

        // 获取当前页面的层次
        const ccId = $('.btn-add').attr('id');

        if (ccId >= 2) { // 判断当前层次大于2就取上一级文件夹的层次
            const up_level = $('.yunpan_li').attr('up_level');
            formData.append("up_level", up_level);
        }


        // 将文件夹名称添加到formData给后台
        formData.append("folderName", folderName);
        formData.append("add_ccId", ccId);

        // const formData = new FormData(this);
        $.ajax({
            url: "/yunpan/add_folder/",
            method: "POST",
            data: formData,
            processData: false,
            contentType: false,
            headers: {
                "X-CSRFToken": "{{ csrf_token }}"
            },
            success: function (response) {
                // 处理成功响应情况
                if (response.success) {
                    alert("表单提交成功！");
                    $(".add_modal").hide();
                    window.location.reload();
                }
            },
            error: function (xhr, status, error) {
                // 处理错误响应情况
                alert("表单提交失败，请重试！");
            }
        });
    });
}

// 获取第二层函数
function getsecond() {
    // 利用事件委托来绑定事件
    $(".yunpan_ul").on('click', '#first_yunpan', function () {
        // console.log(111)
        let dataID = $(this).attr("data-id")
        sessionStorage.setItem('ccID', dataID);  // 将上一级id放在session中，获取方法const storedUserId = sessionStorage.getItem('userId');
        const ccID = sessionStorage.getItem('ccID');

        $.ajax({
            url: '/yunpan/api/getsecond/',
            type: 'POST',
            data: {"id": dataID, "firstID": ccID},
            dataType: 'json',
            success: function (data) {
                // 修改创建文件的id
                $('.btn_sc').attr('id', 2);

                // 修改删除文件的id
                $('.btn-add').attr('id', 2);


                if (data.success) {
                    if ($.isEmptyObject(data.data)) {
                        $('.yunpan_ul li').remove();
                        console.log('返回数据为空');
                        const li = $('<li>').addClass('yunpan_li').attr({"up_level": data.up_level}).html("喔……没文件");
                        $('.yunpan_ul').append(li)
                    } else {
                        $('.yunpan_ul li').remove();
                    }
                    $.each(data.data, function (index, item) {
                        const li = $('<li>').addClass('yunpan_li').attr({
                            "data-id": item.id,
                            "up_level": data.up_level
                        });
                        if (item.file_type_2 === 'folder') {
                            li.attr('id', 'second_yunpan');
                        } else {
                            li.attr('id', 'second_yunpan_file');
                        }
                        const div1 = $('<div>').addClass('li-icon');
                        const symbolId = data.file_type[item.file_type_2]; // 指定 symbol 元素的 ID。获取文件类型，根据后台给定的类型去获取id

                        let iconvHtml;

                        if (item.file_type_2 === 'folder') {
                            iconvHtml = '<svg class="icon svg-icon AL_icon_wjj" aria-hidden="true"><use xlink:href="' + symbolId + '"></use></svg>';
                        } else {
                            iconvHtml = '<svg class="icon svg-icon AL_icon" aria-hidden="true"><use xlink:href="' + symbolId + '"></use></svg>';
                        }

                        // const iconvHtml = '<svg class="icon svg-icon" aria-hidden="true" width="90" height="90"><use xlink:href="' + symbolId + '"></use></svg>';
                        const div2 = $('<div>').addClass("li-title").text(item.file_name);
                        div1.append(iconvHtml).append(div2)
                        li.append(div1).append(div2)

                        let span_lod;
                        let div_but;
                        let a_but;
                        let del_a;
                        let span_del;

                        if (item.file_type_2 !== 'folder') {
                            // 下载按钮
                            div_but = $('<div>').addClass("but_cl")
                            a_but = $('<a>').addClass("load_but").attr({
                                "id": item.id,
                                "leve": 3,
                                "href": "/yunpan/load_file/?id=" + item.id + "&leve=" + 2
                            })
                            span_lod = $('<span>').addClass("glyphicon glyphicon-download-alt").attr("aria-hidden", "true")
                            a_but.append(span_lod)
                            div_but.append(a_but)


                            // 删除按钮
                            del_a = $('<a>').addClass("del_but").attr({
                                "id": item.id,
                                "leve": 3,
                                "href": "/yunpan/del_file/?id=" + item.id + "&leve=" + 2
                            })
                            span_del = $('<span>').addClass("glyphicon glyphicon-trash").attr("aria-hidden", "true")
                            del_a.append(span_del)
                            div_but.append(del_a)


                            li.append(div_but)
                        }

                        $('.yunpan_ul').append(li)

                    });
                } else {
                    console.log(data)
                }
            }
        })
    })
}

// 获取页面数据first，并且渲染上去
function first_xr() {
    $.ajax({
        url: '/yunpan/api/getfirst/',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            // 添加功能标签
            // 创建功能
            const $gn_span_sc_a = $('<a>').addClass('btn_sc').attr({
                "data-toggle": "modal",
                "data-target": "#create_f",
                "id": 1
            });
            const $gn_span_sc = $('<span>').addClass("glyphicon glyphicon-plus-sign").attr("aria-hidden", "true");
            $gn_span_sc_a.append($gn_span_sc);

            // 上传功能  data-toggle="modal" data-target="#eeww"
            const $gn_a = $('<a>').addClass("btn-add").attr({"id": 1});
            const $gn_span = $('<span>').addClass("glyphicon glyphicon-open").attr("aria-hidden", "true");
            $gn_a.append($gn_span);
            $(".fs-key").append($gn_span_sc_a).append($gn_a)

            // 删除firstID，没有不会报错
            sessionStorage.removeItem('ccID');

            // 元素添加完监听添加按钮
            add_btn();
            $.each(data.data, function (index, item) {
                const li = $('<li>').addClass('yunpan_li').attr('id', 'first_yunpan').attr("data-id", item.id);
                const div1 = $('<div>').addClass('li-icon');
                const symbolId = data.file_type[item.file_type_2]; // 指定 symbol 元素的 ID。获取文件类型，根据后台给定的类型去获取id

                let iconvHtml;

                if (item.file_type_2 === 'folder') {
                    iconvHtml = '<svg class="icon svg-icon AL_icon_wjj" aria-hidden="true"><use xlink:href="' + symbolId + '"></use></svg>';
                } else {
                    iconvHtml = '<svg class="icon svg-icon AL_icon" aria-hidden="true"><use xlink:href="' + symbolId + '"></use></svg>';
                }

                // const iconvHtml = '<svg class="icon svg-icon" aria-hidden="true" width="90" height="90"><use xlink:href="' + symbolId + '"></use></svg>';
                const div2 = $('<div>').addClass("li-title").text(item.file_name);
                div1.append(iconvHtml).append(div2)
                li.append(div1).append(div2)


                $('.yunpan_ul').append(li)
            });
        },
        error: function (xhr, status, error) {
            console.error(error);
        }

    });
}


function get_third() {
    $(".yunpan_ul").on('click', '#second_yunpan', function () {
        // console.log(111)
        let dataID = $(this).attr("data-id")
        sessionStorage.setItem('ccID', dataID); // 获取进入第二层的id，给session
        const ccID = sessionStorage.getItem('ccID');

        $.ajax({
            url: '/yunpan/api/getthird/',
            type: 'POST',
            data: {"id": dataID, "firstID": ccID},
            dataType: 'json',
            success: function (data) {
                // 修改创建文件的id
                // $('.btn_sc').attr('id', 3);
                // 最后一层要上传创建文件夹的标签
                $('.btn_sc').remove();

                // 修改删除文件的id
                $('.btn-add').attr('id', 3);


                if (data.success) {
                    if ($.isEmptyObject(data.data)) {
                        $('.yunpan_ul li').remove();
                        console.log('返回数据为空');
                        const li = $('<li>').addClass('yunpan_li').attr({"up_level": data.up_level}).html("喔……没文件");
                        $('.yunpan_ul').append(li)
                    } else {
                        $('.yunpan_ul li').remove();
                    }
                    $.each(data.data, function (index, item) {
                        const li = $('<li>').addClass('yunpan_li').attr({
                            "data-id": item.id,
                            "up_level": data.up_level
                        });
                        if (item.file_type_2 === 'folder') {
                            li.attr('id', 'third_yunpan');
                        } else {
                            li.attr('id', 'third_yunpan_file');
                        }
                        const div1 = $('<div>').addClass('li-icon');
                        const symbolId = data.file_type[item.file_type_2]; // 指定 symbol 元素的 ID。获取文件类型，根据后台给定的类型去获取id

                        let iconvHtml;

                        if (item.file_type_2 === 'folder') {
                            iconvHtml = '<svg class="icon svg-icon AL_icon_wjj" aria-hidden="true"><use xlink:href="' + symbolId + '"></use></svg>';
                        } else {
                            iconvHtml = '<svg class="icon svg-icon AL_icon" aria-hidden="true"><use xlink:href="' + symbolId + '"></use></svg>';
                        }

                        // const iconvHtml = '<svg class="icon svg-icon" aria-hidden="true" width="90" height="90"><use xlink:href="' + symbolId + '"></use></svg>';
                        const div2 = $('<div>').addClass("li-title").text(item.file_name);
                        div1.append(iconvHtml).append(div2)
                        li.append(div1).append(div2)
                        let span_lod;
                        let div_but;
                        let a_but;
                        let del_a;
                        let span_del;

                        if (item.file_type_2 !== 'folder') {
                            // 下载按钮
                            div_but = $('<div>').addClass("but_cl")
                            a_but = $('<a>').addClass("load_but").attr({
                                "id": item.id,
                                "leve": 3,
                                "href": "/yunpan/load_file/?id=" + item.id + "&leve=" + 3
                            })
                            span_lod = $('<span>').addClass("glyphicon glyphicon-download-alt").attr("aria-hidden", "true")
                            a_but.append(span_lod)
                            div_but.append(a_but)


                            // 删除按钮
                            del_a = $('<a>').addClass("del_but").attr({
                                "id": item.id,
                                "leve": 3,
                                "href": "/yunpan/del_file/?id=" + item.id + "&leve=" + 3
                            })
                            span_del = $('<span>').addClass("glyphicon glyphicon-trash").attr("aria-hidden", "true")
                            del_a.append(span_del)
                            div_but.append(del_a)

                            li.append(div_but)
                        }


                        $('.yunpan_ul').append(li)

                    });
                } else {
                    console.log(data)
                }
            }
        })

    })
}

function load_file() {
    // 所有ajax生成的都得用委托事件来获取
    $(document).on('click', '.load_but', function () {
        const id = $(this).closest('.load_but').attr('id');  // 文件id
        const level = $(this).closest('.load_but').attr('leve');  // 文件层次
        $.ajax({
            url: '/yunpan/api/load_file/',
            type: 'POST',
            data: {"id": id, "level": level},
            dataType: 'json',
            xhrFields: {
                responseType: 'blob'
            },
            success: function (blob) {
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
            },
            error: function () {
                alert("下载失败");
            }
        })
    });
}

// $(document).ready(function () {
$(document).ready(function () {

    // 第一层渲染
    first_xr();

    // 监听上传文件提交按钮
    tj_btn();

    // 获取第二层文件
    getsecond();

    // 创建文件夹
    create_folder();

    // 获取第三层监控
    get_third();

    // 下载
    // load_file();
});

