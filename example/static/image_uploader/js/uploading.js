// Create variables (in this scope) to hold the API and image size
var jcrop_api, boundx, boundy, upload_url, form_id;
var image_name, image_id, coord1_id, coord2_id, coord3_id, coord4_id;
var ImageUploader = {
	initCrop: function(min_x, min_y, url, form){
		upload_url = url;
		form_id = form;
		jcrop_api = jQuery.Jcrop('#target', {
			onChange: ImageUploader.updateCrop,
			onSelect: ImageUploader.updateCrop,
			aspectRatio: 16/10,
			minSize: [min_x, min_y],
			bgFade:     true,
			bgOpacity: 0.3,
			boxWidth: 300,
			allowSelect: false	
		});
	  
		// Use the API to get the real image size`
		var bounds = jcrop_api.getBounds();
		boundx = bounds[0];
		boundy = bounds[1];
	},
	
	setInput: function(image_input_name, image_input_id, coord1, coord2, coord3, coord4){
		image_name = image_input_name;
		image_id = image_input_id;
		coord1_id = coord1;
		coord2_id = coord2;
		coord3_id = coord3;
		coord4_id = coord4;
		jQuery(image_id).change(ImageUploader.uploadImage);
	},

	updateCrop: function(c)
	{
	    if (parseInt(c.w) > 0)
	    {
			ImageUploader.changePreview(1, c);
			ImageUploader.changePreview(2, c);
	    }
	    
		jQuery(coord1_id).val(c.x);
		jQuery(coord2_id).val(c.y);
		jQuery(coord3_id).val(c.x2);
		jQuery(coord4_id).val(c.y2);    
	},
	
	changePreview: function(id, c) {
		var w = jQuery('#preview-block_'+id).width()
		var h = jQuery('#preview-block_'+id).height()
		
		var rx = w / c.w;
		var ry = h / c.h;
	
		jQuery('#preview_'+id).css({
			width: Math.round(rx * boundx) + 'px',
			height: Math.round(ry * boundy) + 'px',
			marginLeft: '-' + Math.round(rx * c.x) + 'px',
			marginTop: '-' + Math.round(ry * c.y) + 'px'
		});
	},

	createCroppedImage: function(filename){
		var img = new Image();
		img.src = filename;

		if ($.browser.msie){
		    var w = img.width;
		    var h = img.height;
	    	var mass = [ (w-h/2*1.6)/2, h/4, h/2*1.6+(w-h/2*1.6)/2, h/2 ];
			jcrop_api.setSelect(mass);
		}else{
			$(img).load(function(){
			    var w = img.width;
			    var h = img.height;
		    	var mass = [ (w-h/2*1.6)/2, h/4, h/2*1.6+(w-h/2*1.6)/2, h/2 ];

				jcrop_api.setSelect(mass);
			});						
		}
	},

	uploadImage: function() {
		jQuery(form_id).ajaxSubmit({
			fields: [image_name, 'csrfmiddlewaretoken'],
			url: upload_url,

		    beforeSend: function() {
		    	jQuery('#loading').show();
		    	jQuery('#crop-block').hide();
		    	jQuery('#image-error-block').hide();
		    },
			complete: function (data) {
			    jQuery('#loading').hide();

				var response = jQuery.parseJSON(data.responseText);
			    if(response.success){
			        jQuery('#crop-block').show();

					jcrop_api.setImage(response.filename, function(){
						// Use the API to get the real image size
						var bounds = this.getBounds();
						boundx = bounds[0];
						boundy = bounds[1];

						ImageUploader.createCroppedImage(response.filename);
					});
			        jQuery("[id^='preview_']").attr('src', response.filename);
			    } else {
			    	jQuery(image_id).replaceWith(jQuery(image_id).clone());
			    	jQuery(image_id).change(ImageUploader.uploadImage);
			    	
			        jQuery('#image-error-block').show();
			        jQuery('#image-error').text(response.message);
			    }	
			}
		})
	}
}