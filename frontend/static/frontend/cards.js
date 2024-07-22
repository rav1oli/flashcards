function flip(card){
    // shenaningans to make animation replay
    domCard = card[0];

    void domCard.offsetWidth;
    card.addClass('flipping');

    //this is unbelievably scuffed
    setTimeout(() => {
        if(card.hasClass('flipped')){
            card.removeClass('flipped')
        }   
        else {
            card.addClass('flipped');
        }
    }, 150);

    setTimeout(() => {
        card.removeClass('flipping');
    }, 300);
}

$(function() {

    $('.flip-icon').each(function(){
        $(this).on('click', function(e){

            e.stopPropagation();
            flip($(this).parent('.card'));

        });
    });

    $('.card').each(function(){
        $(this).on('click', function(e){
            $(this).toggleClass('selected');
        })
    })

});