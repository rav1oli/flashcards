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

jQuery(function() {

    jQuery('.flip-icon').each(function(){
        jQuery(this).on('click', function(e){

            e.stopPropagation();
            flip(jQuery(this).parent('.card'));

        });
    });

});