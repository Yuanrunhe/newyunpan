// 项目添加
function bindBtnAddEvent() {
    $.ajax({
        url: "/add_project/",
        type: "POST",
        data: new FormData($("#add_form")[0]),
        dataType: "JSON",
        processData: false,
        contentType: false,
        beforeSend: function () {
            $.LoadingOverlay("show");
        },
        success: function (res) {
            window.location.reload();
        },
        error: function (xhr, status, error) {
            $('.error-ts').html("")
            var errors = JSON.parse(xhr.responseText).errors;
            console.log(errors);
            for (var field in errors) {
                if (errors.hasOwnProperty(field)) {
                    var errorMessages = errors[field];
                    var field_id = $("#" + field);
                    field_id.html(errorMessages);
                }
            }
        },
        complete: function () {
            // 隐藏加载指示器
            $.LoadingOverlay("hide");
        }
    });
}


// 项目修改
$(function () {
    $('.edit-btn').click(function () {
        var id = $(this).data('id');
        $.ajax({
            url: '/edit_project/',
            type: 'GET',
            dataType: 'json',
            data: {'id': id},
            success: function (response) {
                // 获取模态框的位置
                let edm = $('#editModal');
                // 将内容渲染进去，记得后端返回应该是form.as_p()
                // edm.find('.modal-body').find('#edit_form').html(response.form);
                edm.find('.modal-body').find('#edit_form').find(".modal-body1").html(response.form);

                // 保存选项
                $('#save-btn').click(function () {
                    $.ajax({
                        url: '/edit_project/',
                        type: 'POST',
                        data: new FormData($("#edit_form")[0]), // 得用这种方法才能拿到上传得文件
                        // data:  $('#edit_form').serialize(), // 得用这种方法才能拿到上传得文件
                        dataType: "JSON",
                        processData: false,
                        contentType: false,
                        success: function (response) {
                            console.log(1111)
                            if (response.success) {
                                // 验证成功，关闭弹框并刷新页面
                                $('#editModal').modal('hide');
                                location.reload();
                            } else {
                                // 验证失败，显示错误信息
                                edm.find('.error').remove();
                                console.log(response.errors)
                                for (var field_name in response.errors) {
                                    var field_errors = response.errors[field_name];
                                    var field_input = $('#editModal').find('[name=' + field_name + ']');
                                    field_input.after('<span class="error">' + field_errors.join(', ') + '</span>');
                                }
                            }
                        }
                    });
                });
                edm.modal('show');  // 显示模块
            }
        });
    });
});

// 项目删除
$(function () {
    $(".del-btn").click(function () {
        const id = $(this).data('id');
        console.log(id)
        const edm = $('#delModal');
        edm.modal('show');  // 显示模块
        $('#del-btn').click(function () {
            $.ajax({
                url: '/del_project/',
                type: 'POST',
                data: {'id': id},
                dataType: "JSON",
                success: function (response) {
                    if (response.success) {
                        $('#delModal').modal('hide');
                        location.reload();
                    } else {
                        alert("删除失败")
                    }
                }
            });
            $('#delModal').modal('show');
        });
    })
})

// 图书按钮监听
$(function (){
    $('.addbtn').click(function () {
                $('#add_err')[0].innerHTML = "";
    })
});

// 添加笔记
function addNote() {
    // const formData = new FormData(this);
    const errpt = $('#add_err');
    $.ajax({
        url: '/add_note/',
        type:'POST',
        data: new FormData($("#addModelForm").get(0)),
        // data: formData,
        dataType: "JSON",
        processData: false,
        contentType: false,
        success: function (response) {
            errpt.empty();
            if (response.success) {
                window.location.reload()
            }else {
                // $('.adderr').after('<span id="add_err" style="color: red">'+response.err+'</span>')
                errpt[0].innerHTML = response.err
            }
        }
    })
}

// 笔记删除
$(function () {
    $(".delbtn").click(function () {
        $("#note_del_Modal").modal('show');
        const id = $(this).data('id');
        $('.note_del').click(function () {
            $.ajax({
                url: "/del_note/",
                data: {"id": id},
                type: 'POST',
                dataType: "JSON",
                success: function (response) {
                    if (response.success) {
                        window.location.reload()
                        console.log("成功");
                    }else {
                        console.log("失败")
                    }
                }
            })
        })
    });
});