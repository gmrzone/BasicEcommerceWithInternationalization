// Navigation dropdown script

$(document).ready(function(){
    var backmodel = document.querySelector('.backdrop')
    
    $('.dropdown').click(function(){
        
        const d = this.children[1].style.display
        

        if (d == 'block'){
            $(this).children('.dropdowm-content').css('display', 'none');
            backmodel.style.display = "none";
        }
        else {
            $('.dropdowm-content').css('display', 'none');
            $(this).children('.dropdowm-content').css('display', 'block');
            backmodel.style.display = "block";
        }
        
    })
//  backdrop for dropdown menu so we can click anywhere and close dropdoewn
    $('.backdrop').click(function(){
        var afzal = document.querySelectorAll('.dropdowm-content');
        
        for (var i = 0; i < afzal.length; i++){
            if(afzal[i].style.display == 'block'){
                afzal[i].style.display = 'none';
                backmodel.style.display = "none";
            }
        }

    })

    $('.mobile-nav-close').click(function(){
        close_mobile_nav()
    })

//  backdrop for mobile nav
    $(".backdrop1").click(function(){
        if ($('.nav-content')) {
            close_mobile_nav()
        }
    })

    $('.mob-nav-opener').click(function(){
            open_mobile_nav();
    })

    function open_mobile_nav(){
        $('.nav-content').css('display', 'flex')
        $('.backdrop1').css('display', 'block')


        window.setTimeout(function(){

            $('.nav-content').css('width', '300px')
            $('.nav-content').css('opacity', '1')
            $('.backdrop1').css('opacity', '1')
        }, 10);


    }
    function close_mobile_nav(){

        $('.nav-content').css('width', '0px')
        $('.nav-content').css('min-width', '0px')
        $('.backdrop1').css('opacity', '0')


        window.setTimeout(function(){
            $('.nav-content').css('display', 'none')
            $('.backdrop1').css('display', 'none')
        }, 200);
    }

});
