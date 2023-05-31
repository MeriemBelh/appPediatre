$(function(){
    $("#form-total").steps({
        headerTag: "h2",
        bodyTag: "section",
        transitionEffect: "fade",
        //enableAllSteps: true,
        autoFocus: true,
        transitionEffectSpeed: 500,
        titleTemplate : '<div class="title">#title#</div>',
        labels: {
            previous : '<i class="fa fa-arrow-left"></i>',
            next : '<i class="fa fa-arrow-right"></i>',
            finish : '<i class="fa fa-check"></i>',
            current : ''
        },
        onStepChanging : function (event, currentIndex, newIndex) {

            $("#form-register").validate().settings.ignore = ":disabled,:hidden";
            return $("#form-register").valid();

        },
        onFinished: function(e, currentIndex) {
            return $("#form-register").submit();
        }

    });
});
