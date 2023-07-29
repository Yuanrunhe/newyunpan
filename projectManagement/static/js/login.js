// 获取输入框元素
// const usernameInput = document.getElementById('username');
// const passwordInput = document.getElementById('password');
// const captchaInput = document.getElementById('captcha');
//

$(document).ready(function () {
    const captchaImg = $('#captcha-img');

// 鼠标悬停时显示提示
    captchaImg.on('mouseover', function () {
        captchaImg.attr('title', '点击刷新验证码');
    });

// 鼠标离开时移除提示
    captchaImg.on('mouseout', function () {
        captchaImg.removeAttr('title');
    });


    captchaImg.on('click', function () {
        const imgElement = $(this);
        $.ajax({
            url: '/image/code/',
            method: 'GET',
            responseType: 'arraybuffer',
            success: function (response) {
                const blob = new Blob([response], {type: 'image/png'});
                const imgUrl = URL.createObjectURL(blob);
                // imgElement.attr('src', imgUrl);
                imgElement.attr('src', '/image/code/');
            },
            error: function (xhr, status, error) {
                console.log('Error:', error);
            }
        });
    });
})
