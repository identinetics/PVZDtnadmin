let $ = django.jQuery;
$(document).ready(function() {

  $('a[href="#sign"]').click(function(){
    $.ajax({
      type: "GET",
      dataType : 'xml',
      url: $('#ed_uploaded_get_template_url').text(),
      success: function(dataXML){
        $.ajax({
           type: 'POST',
           // make sure you respect the same origin policy with this url:
           url: 'http://192.168.1.107:13495/http-security-layer-request',
           // url: 'http://127.0.0.1:3495/http-security-layer-request',
           contentType: 'application/x-www-form-urlencoded',
           processData: false,
           data: 'XMLRequest=' + new XMLSerializer().serializeToString(dataXML.documentElement),
           success: function(msg){
                alert(msg);
                // TODO get sign result and post to admin
            },
           error: function(e, exception){
             if (exception == 'error'){
               alert('Sign service does not respond')
             }
             else {
               console.log('error signing');
             }
            }
        });
      },
      error : function(e, exception){
        console.log(e);
        console.log(exception);
        console.log('error downloading');
      }
    });
  });
});