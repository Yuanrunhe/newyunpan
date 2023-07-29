// 原先菜单开启关闭事件的js
// menuItems1 = document.querySelectorAll(".menu-item");
// menuItems1.forEach((menuItem) => {
//   const submenu = menuItem.querySelector(".sub-menu");
//   if (submenu) {
//     menuItem.addEventListener("click", () => {
//       if (submenu.style.display === "block") {
//         submenu.style.display = "none";
//       } else {
//         closeAllSubmenus();
//         submenu.style.display = "block";
//       }
//     });
//   }
// });
//
// function closeAllSubmenus() {
//   const submenus = document.querySelectorAll(".sub-menu");
//   submenus.forEach((submenu) => {
//     submenu.style.display = "none";
//   });
// }
// 到这里




// 下面是菜单栏的请求并且渲染脚本

$(document).ready(function() {
    $.ajax({
        url: '/menu/', // 将 URL 替换为视图函数的 URL。
        dataType: 'json',
        success: function(data) {
            renderMenu(data.menu);
        },
        error: function() {
            console.log('Error retrieving menu data.');
        }
    });
});

function renderMenu(menu) {
    const $menu = $('#menu');
    $menu.empty(); // 清空之前可能存在的菜单项
    for (const item in menu) {
        const $li = $('<li></li>').attr("class","first_label");
        const $a = $('<a></a>').attr('href', menu[item].url).text(menu[item].name);
        $li.append($a);
        if (menu[item].children.length > 0) {
            const $ul = $('<ul></ul>');
            for (let i = 0; i < menu[item].children.length; i++) {
                const child = menu[item].children[i];
                const $childLi = $('<li></li>').attr("class","Secondary_label");
                const $childA = $('<a></a>').attr('href', child.url).text(child.name);
                $childLi.append($childA);
                $ul.append($childLi);
            }
            $li.append($ul);
        }
        $menu.append($li);
    }
}


// 获取所有一级菜单项
const menuItems2 = document.querySelectorAll('.first_label');

// 循环遍历每个一级菜单项
menuItems2.forEach(item => {
  // 监听菜单项的点击事件
  item.addEventListener('click', () => {
    // 获取当前菜单项包含的二级菜单
    const subMenu = item.querySelector('.Secondary_label');

    if (subMenu) {
      // 切换二级菜单的显示与隐藏状态
      subMenu.classList.toggle('active');
    }
  });
});