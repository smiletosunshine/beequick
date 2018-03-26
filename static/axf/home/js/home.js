$(document).ready(function(){
    swiper1()
    swiper2()
});


function swiper1(){
    var swiper = new Swiper("#topSwiper", {
        direction: "horizontal",
        loop: true,
        speed: 500,
        autoplay: 2000
    });
}
function swiper2(){
    var swiper = new Swiper("#menuSwiper", {
        slidesPerView: 3,
        spaceBetween: 2,
        loop: false,
    });
}

