let leftSidebarClose = document.querySelector('#leftSidebarClose');
let leftSidebarOpen = document.querySelector('#leftSidebarOpen');
let rightSidebarClose = document.querySelector('#rightSidebarClose');
let rightSidebarOpen = document.querySelector('#rightSidebarOpen');
let rightSidebarDesktopOpen = document.querySelector('#rightSidebarDesktopOpen');

let leftSidebar = document.querySelector('#leftSidebar');
let rightSidebar = document.querySelector('#rightSidebar');

function closeSidebar(sidebar) {
    sidebar.classList.remove('active');
    sidebar.classList.add('close');
}

function openSidebar(sidebar) {
    sidebar.classList.remove('close');
    sidebar.classList.add('active');
}

leftSidebarClose.addEventListener('click', () => {
    closeSidebar(leftSidebar);
});

leftSidebarOpen.addEventListener('click', () => {
    openSidebar(leftSidebar);
});

if (rightSidebarClose && rightSidebarOpen && rightSidebarDesktopOpen) {
    rightSidebarClose.addEventListener('click', () => {
        closeSidebar(rightSidebar);
        setTimeout(() => {
            rightSidebar.classList.toggle('d-none');
        }, 500);
    });
    rightSidebarDesktopOpen.addEventListener('click', (e) => {
        e.preventDefault();
        rightSidebar.classList.toggle('d-none');
        openSidebar(rightSidebar);
    });
    rightSidebarOpen.addEventListener('click', (e) => {
        e.preventDefault();
        rightSidebar.classList.toggle('d-none');
        openSidebar(rightSidebar);
    });
}


