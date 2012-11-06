if (jQuery == undefined && django.jQuery != undefined){
    var jQuery = django.jQuery;
}

var MakeClass = function(){
    return function( args ){
        if( this instanceof arguments.callee ){
            if( typeof this.__construct == "function" ) this.__construct.apply( this, args );
        }else return new arguments.callee( arguments );
    };
}


var NewClass = function( variables, constructor, functions ){
    var retn = MakeClass();
    for( var key in variables ){
        retn.prototype[key] = variables[key];
    }
    for( var key in functions ){
        retn.prototype[key] = functions[key];
    }
    retn.prototype.__construct = constructor;
    return retn;
}

jQuery(document).ready(function(){
    if (window.croppers != undefined){
        for(var i = 0; i < window.croppers.length; i++){
            var cropper = window.croppers[i];
            var target = jQuery('#' + cropper.id + '-target')
            cropper.jcrop_api = jQuery.Jcrop(target, {
                onChange: cropper.updateCrop.bind(cropper),
                onSelect: cropper.updateCrop.bind(cropper),
                aspectRatio: cropper.size[0] / cropper.size[1],
                minSize: cropper.size,
                bgFade:     true,
                bgOpacity: 0.3,
                boxWidth: cropper.width,
                allowSelect: false
            })
            var bounds = cropper.jcrop_api.getBounds();
            cropper.boundx = bounds[0];
            cropper.boundy = bounds[1];
            // if (target.attr('src')){
            //     cropper.jcrop_api.setSelect([0, 0, target.width(), target.height()]);
            // }
        }
    }
});


var Cropper = NewClass( {
}, function( id, size, width, url ){/*Function constructor of class*/
    this.upload_url = url
    this.id = id;
    this.image = jQuery('#' + id + '_0');
    this.coord1 = jQuery('#' + id + '_1');
    this.coord2 = jQuery('#' + id + '_2');
    this.coord3 = jQuery('#' + id + '_3');
    this.coord4 = jQuery('#' + id + '_4');
    this.edit_mode = jQuery('#' + id + '_5');
    this.form = this.image.parents("form");
    this.size = size;
    this.width = width;

    this.crop_block = jQuery('#' + id + '-crop-block');
    this.loading_image = jQuery('#' + id + '-loading');
    this.error_block = jQuery('#' + id + '-error-block');
    this.error_text = jQuery('#' + id + '-error-text');

    var self = this;
    this.image.change(function() {
        self.edit_mode.attr('checked', false);
        self.form.ajaxSubmit({
            fields: [self.image.attr('name'), 'csrfmiddlewaretoken'],
            url: self.upload_url,

            beforeSend: function() {
                self.loading_image.show();
                self.crop_block.hide();
                self.error_block.hide();
            },
            complete: function (data) {
                self.loading_image.hide();

                var response = jQuery.parseJSON(data.responseText);
                if(response.success){
                    self.crop_block.show();
                    self.jcrop_api.setImage(response.filename, function(){
                        // Use the API to get the real image size
                        var bounds = self.jcrop_api.getBounds();
                        self.boundx = bounds[0];
                        self.boundy = bounds[1];

                        // create a cropped image
                        var img = new Image();
                        img.src = response.filename;

                        select = function(w, h){
                            var ratio = self.size[0] / self.size[1]
                            var a, b
                            if (h <= w) {
                                b = Math.max(self.size[1], 3*h/4);
                                a = b * ratio;
                            } else {
                                a = Math.max(self.size[0], 3*w/4);
                                b = a / ratio;
                            }
                            var mass = [(w-a)/2, (h-b)/2, (w-a)/2+a, (h-b)/2+b];
                            self.jcrop_api.setSelect(mass);
                        }

                        if (jQuery.browser.msie){
                            var w = img.width;
                            var h = img.height;
                            select(w, h)
                        }else{
                            jQuery(img).load(function(){
                                var w = img.width;
                                var h = img.height;
                                select(w, h)
                            });
                        }
                    });
                    jQuery('.' + self.id + '-preview-wrap').each(function() {
                        jQuery(this).children('img').attr('src', response.filename);
                    })
                } else {
                    (self.image).replaceWith(self.image.clone(true));

                    self.crop_block.hide();
                    self.error_block.show();
                    self.error_text.text(response.message);
                }
            }
        })
    });

},{/*Class methods*/
    "updateCrop": function(c){
        // TODO: preview outer div must have id-preview-wrap class!
        if (parseInt(c.w) > 0)
        {
            var self = this;
            jQuery('.' + this.id + '-preview-wrap').each(function() {
                var w = jQuery(this).width()
                var h = jQuery(this).height()

                var rx = w / c.w;
                var ry = h / c.h;

                jQuery(this).children('img').css({
                    width: Math.round(rx * self.boundx) + 'px',
                    height: Math.round(ry * self.boundy) + 'px',
                    marginLeft: '-' + Math.round(rx * c.x) + 'px',
                    marginTop: '-' + Math.round(ry * c.y) + 'px'
                });
            });
        }

        this.coord1.val(c.x);
        this.coord2.val(c.y);
        this.coord3.val(c.x2);
        this.coord4.val(c.y2);
    }
});
