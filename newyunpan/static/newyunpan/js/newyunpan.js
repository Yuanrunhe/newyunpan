// 上传文件按钮
function getModel() {
    $(".btn-sc-file").click(function () {
        $('#cr-wjj-qrsc').hide();
        $('#up-file-qrsc').show();
        $.ajax({
            url: '/newyp/upfile/',
            type: 'GET',
            success: function (response) {
                $('#sc-modelLabel').text("上传文件")
                $('.sc-model-body').html(response);  // 将返回的HTML填充到模态框中的内容区域
                $('#sc-model').modal('show');
            }
        })
    })
}

function qr_up_file() {
    $("#up-file-qrsc").click(function () {
        const fileInput = document.getElementById('id_directory');
        if (fileInput.files.length === 0) {
            alert('请先选择文件');
            return; // 终止函数执行
        }
        const file = fileInput.files[0];  // 获取文件
        const ulId = $('.file-all-ul').attr('id');
        // 创建 FormData 对象
        const formData = new FormData();
        // 添加文件和其他表单字段的值
        formData.append('file', file);
        formData.append('fileType', file.type);
        formData.append('fileSize', file.size);
        formData.append('levelID', ulId);
        formData.append('filename', file.name);
        $.ajax({
            url: '/newyp/upfile/',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                $('#sc-model').modal('hide');
                // 回调重新渲染页面
                const ulID = $('.file-all-ul').attr('id');
                getPageData(ulID);
            },
            error: function (xhr, status, error) {
                alert("上传失败");
                $('#sc-model').modal('hide');
                const ulID = $('.file-all-ul').attr('id');
                getPageData(ulID);
            }
        });
    })
}

function create_wjj() {
    $(".btn-cj-wjj").click(function () {
        $('#up-file-qrsc').hide();
        $('#cr-wjj-qrsc').show();
        $.ajax({
            url: '/newyp/crFolder/',
            type: 'GET',
            success: function (response) {
                $('#sc-modelLabel').text("创建文件夹");
                $('.sc-model-body').html(response);  // 将返回的HTML填充到模态框中的内容区域
                $('#sc-model').modal('show');
            }
        })
    })
}

// 字符串判断
function isAllSymbols(input) {
    const regex = /^[^\u4E00-\u9FFF\w\s]+$/;
    return regex.test(input);
}

// 创建文件
function cr_wjj_file() {
    $("#cr-wjj-qrsc").click(function () {
        const inputValue = $('#create_folder_name').val();
        if (inputValue === '') {
            alert('输入框不能为空！');
            return 0
        } else if (inputValue.replace(/\s/g, '') === '') {
            alert('输入内容不能只包含空格！');
            return 0
        } else if (isAllSymbols(inputValue)) {
            alert('输入内容不能全为符号！');
            return 0
        }

        const ulId = $('.file-all-ul').attr('id');
        const formData = new FormData();
        formData.append("folderName", inputValue);
        formData.append("folderLevel", ulId);
        $.ajax({
            url: '/newyp/crFolder/',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                // console.log(response);
                const fieldValue = response.message;
                alert(fieldValue);
                $('#sc-model').modal('hide');
                // 回调重新渲染页面
                const ulID = $('.file-all-ul').attr('id');
                getPageData(ulID);
            },
            error: function (xhr, status, error) {
                console.log(xhr.responseText);
                alert("创建失败");
            }
        });
    })
}

// get page data  参数为当前的文件夹id
function getPageData(pageWJJID) {
    const WJJID = pageWJJID;
    // 上传文件按钮的显示隐藏
    if (WJJID === 'file-first') {
        $('.btn-sc-file').hide();
        rtupbtn(WJJID);
    }
    const formData = new FormData();
    formData.append("folderID", WJJID);
    $.ajax({
        url: '/newyp/getPageFile/',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function (response) {
            if (WJJID === 'file-first') {
                $('.btn-sc-file').hide();
            } else {
                $('.btn-sc-file').show();
            }
            rtupbtn(WJJID);
            const ulBQ = $('.file-all-ul');
            ulBQ.empty();
            ulBQ.attr('id', WJJID);
            const FolderDict = response.FolderDict;
            const FileDict = response.FileDict;
            // 渲染文件夹
            if (FolderDict !== "None") {
                $.each(FolderDict, function (index, item) {
                    // console.log(index)
                    const li = $('<li>').attr({
                        "id": index,
                        "name": item,
                        "class": 'folder'
                    });
                    const iconvHtml = '<svg class="icon al-icon-wjj" aria-hidden="true"><use xlink:href="#icon-wenjianjia"></use></svg>';
                    const divTitle = $('<div>').addClass("file-title").text(item);
                    li.append(iconvHtml);
                    li.append(divTitle);
                    $('.file-all-ul').append(li);
                });
            }

            // 渲染文件
            if (FileDict !== "None") {
                $.each(FileDict, function (index, item) {
                    const li = $('<li>').attr({
                        "id": index,
                        // "name": item,
                        "name": item.fileName,
                        "class": 'file'
                    });

                    // 下载按钮
                    const downIcon = $('<div>').addClass("download-icon").attr({'downID':index});
                    const downA = $('<a>').attr({"href": '/newyp/fileDown/?fileID=' + index});
                    const downIcon2 = $('<span>').addClass("glyphicon glyphicon-download-alt");
                    downA.append(downIcon2);
                    downIcon.append(downA);

                    // 删除按钮
                    const trashIcon = $('<div>').addClass("trashload-icon").attr({'trashID':index});
                    const trashIcon2 = $('<span>').addClass("glyphicon glyphicon-trash")
                    trashIcon.append(trashIcon2);


                    const iconvHtml = '<svg class="icon al-icon-file" aria-hidden="true"><use xlink:href='+item.fileType+'></use></svg>';
                    const divTitle = $('<div>').addClass("file-title").text(item.fileName);
                    li.append(iconvHtml);
                    li.append(divTitle);
                    li.append(downIcon);
                    li.append(trashIcon);
                    $('.file-all-ul').append(li);
                });
            }
        },
        error: function (xhr, status, error) {
            console.log(xhr.responseText)
        }
    });
}

// 获取文件夹内容
function selectFolder() {
    $(document).on('click', '.folder', function () {
        const ulID = $('.file-all-ul').attr('id');
        const folderID = $(this).attr('id');
        getPageData(folderID);
    });
}

// 上一级按钮,显示及关闭
function rtupbtn(ulId){
    // 上传文件按钮的显示隐藏
    if (ulId === 'file-first') {
        $('#rtupID').prop('disabled', true);
    }else {
        $('#rtupID').prop('disabled', false);
    }
}

// 返回上一层
function rtupsx() {
    $(document).on('click', '#rtupID', function () {
        const levelID = $('.file-all-ul').attr('id');
        const formData = new FormData();
        formData.append("levelID",levelID);
        $.ajax({
            url: '/newyp/rtupData/',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                getPageData(response.upLevelID);
            },
            error: function (xhr, status, error) {
                console.log(xhr);
            }
        });
    })
}

// 获取文件夹内容
function downfile() {
    $(document).on('click', '.download-icon', function () {
        const fileID = $(this).attr('downid');
        console.log(fileID)
        // const formData = new FormData();
        // formData.append('fileID',fileID);
        $.ajax({
            url: '/newyp/fileDown/',
            type: 'GET',
            data: { "fileID": fileID},
            dataType: 'json',
            success: function (response) {
                console.log(response)
            },
            error: function (xhr, status, error) {
                console.log(xhr);
            }
        });
    });
}

$(document).ready(function () {
    getPageData('file-first');
    getModel();
    qr_up_file();
    create_wjj();
    cr_wjj_file();
    selectFolder();
    rtupsx();
    // downfile();
});
// $(document).ready(function() {
//   $('.menu li').hover(
//     function() {
//       $(this).find('.submenu').slideDown();
//     },
//     function() {
//       $(this).find('.submenu').slideUp();
//     }
//   );
// });




$(document).ready(function() {
  $('.menu li').click(function(e) {
    e.stopPropagation();
    var submenu = $(this).find('.submenu');

    if (submenu.is(':visible')) {
      submenu.slideUp();
    } else {
      $('.menu li .submenu').not(submenu).slideUp();
      submenu.slideDown();
    }

    $('.menu li').not(this).find('.submenu').slideUp();
  });

  $(document).click(function() {
    $('.menu li .submenu').slideUp();
  });
});




