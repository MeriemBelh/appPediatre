$(function(){
    $("#form-register").validate({
        rules: {
            tele:{
                minlength:10, maxlength:10
            },
            tele1: {
                minlength:10, maxlength:10
            },
            delegation: {
                required: true
            },
            CM:{
                required: true
            },
            PS :{
                required: true
            },
            A_M_A :{
                required: true
            },
            GS :{
                required: true
            },
            TG :{
                required: true
            },
            AV :{
                required: true
            },
            SN :{
                required: true
            },
            PN :{
                required: true
            },
            TN :{
                required: true
            },
            NHA :{
                required: true
            },
            All :{
                required: true
            },
            DA :{
                required: true
            },
            RSP :{
                required: true
            }
        },
        messages: {
            Nom: {
                required: "Veuillez saisir le nom"
            },
            Prenom: {
                required: "Veuillez saisir le prénom"
            },
            adresse: {
                required: "Veuillez saisir l'adresse"
            },
            ville: {
                required: "Veuillez saisir la ville"
            },
            delegation:{
                required: "Veuillez choisir une délégation"
            },
            tele:{
                required: "Veuillez entrer le n° de téléphone"

            },
            tele1:{
                required: "Veuillez entrer le n° de téléphone"

            },
            date_naissance:{
                required: "Veuiller entrer la date de naissance"
            },
            CM:{
                required: "Veuiller Choisir un champs "
            },
            PS :{
                required: "Veuiller Choisir un champs "
            },
            GS :{
                required: "Veuiller Choisir un champs "
            },
            TG :{
                required: "Veuiller Choisir un champs "
            },
            AV :{
                required: "Veuiller Choisir un champs "
            },
            SN :{
                required: "Veuiller Choisir un champs "
            },
            PN :{
                required: "Veuiller Choisir un champs "
            },
            TN :{
                required: "Veuiller Choisir un champs "
            },
            All :{
                required: "Veuiller Choisir un champs "
            },
            RSP :{
                required: "Veuiller Choisir un champs "
            }

        }
    });
    $("#form-total").steps({
        headerTag: "h2",
        bodyTag: "section",
        transitionEffect: "fade",
        // enableAllSteps: true,
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
            var Nom = $('#Nom').val();
            var Prenom = $('#Prenom').val();
            var tele = $('#tele').val();
            var tele1 = $('#tele1').val();
            var delegation = $('#delegation').val();
            var CM = $("input[name='CM']:checked").val();
            var ville = $('#ville').val();
            var adresse = $('#adresse').val();
            var date_naissance = $('#date_naissance').val();

            var AAA = $('#AAA').val();
            var ASA = $('#ASA').val();
            var MS = $('#MS').val();
            var MP = $('#MP').val();
            var DAA = $('#DAA').val();
            var DSA = $('#DSA').val();
            var PSy = $('#PSy').val();
            var PM = $('#PM').val();
            var PP = $('#PP').val();
            var SA = $('#SA').val();
            var PEA = $('#PEA').val();
            $('#nom-val').text(Nom);
            $('#Prenom-val').text(Prenom);
            $('#tele-val').text(tele);
            $('#tele1-val').text(tele1);
            $('#ville-val').text(ville);
            $('#delegation-val').text(delegation);
            $('#CM-val').text(CM);
            $('#adresse-val').text(adresse);
            $('#date_naissance-val').text(date_naissance);
            $('#PS-val').text(PS);
            $('#A_M_A-val').text(A_M_A);
            $('#GS-val').text(GS);
            $('#TG-val').text(TG);
            $('#AV-val').text(AV);
            $('#SN-val').text(SN);
            $('#PN-val').text(PN);
            $('#TN-val').text(TN);
            $('#NHA-val').text(NHA);
            $('#All-val').text(All);
            $('#DA-val').text(DA);
            $('#RSP-val').text(RSP);
            $('#AAA-val').text(AAA);
            $('#ASA-val').text(ASA);
            $('#PP-val').text(PP);
            $('#PM-val').text(PM);
            $('#DAA-val').text(DAA);
            $('#DSA-val').text(DSA);
            $('#PSy-val').text(PSy);
            $('#SA-val').text(SA);
            $('#PEA-val').text(PEA);
            $('#MS-val').text(MS);
            $('#MP-val').text(MP);
            $("#form-register").validate().settings.ignore = ":disabled,:hidden";
            return $("#form-register").valid();

        },
        onFinished: function(e, currentIndex) {
            return $("#form-register").submit();
        }
    });
});

/*$(function(){
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
*/