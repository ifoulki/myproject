<x-layoutAdm page='نشر فيديو جديد'>

    <section class="content">
        <article>
        <h1><i class="fas fa-video"></i> نشر فيديو جديد</h1>
        @if (Auth::user()->role != "admin")
            <label class="label">
                <i class="fas fa-user"></i>
                {{ Auth::user()->Prenom .' '. Auth::user()->Nom }}
            </label>
        @endif

        <form method="POST" enctype="multipart/form-data" action="{{ route('auth.videos.store') }}">
            @csrf

            <div class="form">
                <label class="label">
                    <i class="fas fa-upload"></i> تحميل صورة:
                </label>

                <div class="mb-3">
                    <input class="form-control" type="file" id="formFile" name="Myimage">
                </div>

                <img id="imagePreview" class="image-preview" alt="معاينة الصورة" style="display: none;">
                @error('Myimage')
                    <small class="text-danger">{{ $message }}</small>
                @enderror
            </div>

            <hr>

            <div class="form">
                <label class="label">
                    <i class="fas fa-heading"></i> عنوان فيديو:
                </label>
                <input
                    type="text"
                    name="title"
                    placeholder="عنوان فيديو ..."
                    minlength="5"
                    class="title form-control"
                    value="{{ old('title') }}"
                >
                @error('title')
                    <small class="text-danger">{{ $message }}</small>
                @enderror
            </div>

            <hr>

                <div class="form">
                    <label class="label"><i class="fas fa-language"></i>  العنوان مكتوب بأي لغة ؟ </label>
                    <select class="small-input @error('dir') is-invalid @enderror" name="dir">
                        <option value="" disabled selected>اختر اللغة</option>
                        <option value="rtl" {{ old('dir') === 'rtl' ? 'selected' : '' }}>العربية</option>
                        <option value="ltr" {{ old('dir') === 'ltr' ? 'selected' : '' }}>Français</option>
                        <option value="ltr" {{ old('dir') === 'ltr' ? 'selected' : '' }}>English</option>
                    </select>
                    @error('dir')
                            <small class="text-danger">{{ $message }}</small>
                    @enderror
                </div>

            <hr>

            @if (Auth::user()->role == "admin")
                <div class="form">
                    <label class="label">
                        <i class="fas fa-user"></i> اسم الكاتب :
                    </label>
                    <input 
                        type="text" 
                        name="Author"
                        placeholder="اسم الكاتب ..."
                        minlength="5"
                        class="author form-control"
                        value="{{ old('author') ?? Auth::user()->Prenom .' '. Auth::user()->Nom  }}"
                    />
                </div>
            @else 
                <input 
                    type="hidden" 
                    name="Author"
                    placeholder="اسم الكاتب ..."
                    minlength="5"
                    class="author form-control"
                    value="{{ Auth::user()->Prenom .' '. Auth::user()->Nom }}"
                />
            @endif
            @error('Author')
                <small class="text-danger">{{ $message }}</small>
            @enderror

            <hr>

            <div class="form">
                <label class="label">
                    <i class="fas fa-paperclip"></i> رابط الفيديو:
                </label><br>
                <input
                    name="Mysubject"
                    id="video_url"
                    placeholder="أدخل رابط يوتيوب هنا"
                    class="form-control"
                    value="{{ old('Mysubject') }}"
                >
                @error('Mysubject')
                    <small class="text-danger">{{ $message }}</small>
                @enderror
                
                <div id="videoPreview" style="margin-top: 10px;"></div>
            </div>

            <hr>

            <div class="form">
                <label class="label">
                    <i class="fas fa-align-right"></i> وصف مرفق للفيديو سيظهر أسفله:
                </label><br>
                <textarea
                    name="autre"
                    id="autreInput"
                    class="form-control textarea-container"
                    placeholder="أكتب أكواد html، لإرفاق صور أو كتب ... إلخ"
                >{{ old('autre') }}</textarea>
                @error('autre')
                    <small class="text-danger">{{ $message }}</small>
                @enderror
            </div>

            <hr>

            <div class="mb-3 form">
                    <label for="educational_level" class="form-label">
                        <i class="fas fa-graduation-cap"></i>هل يجب أن يكون للمشاهدين مستوى دراسي محدد؟
                    </label>
                    
                    <select id="educational_level" name="educational_level" class="form-select">
                        <option value="Unknown" {{ old('educational_level') == 'Unknown' ? 'selected' : '' }}>لا، المقال مناسب للجميع</option>
                        <optgroup label="الإبتدائي :">
                            <option value="1st Year of Primary School" {{ old('educational_level') == '1st Year of Primary School' ? 'selected' : '' }}>السنة الأولى ابتدائي</option>
                            <option value="2nd Year of Primary School" {{ old('educational_level') == '2nd Year of Primary School' ? 'selected' : '' }}>السنة الثانية ابتدائي</option>
                            <option value="3rd Year of Primary School" {{ old('educational_level') == '3rd Year of Primary School' ? 'selected' : '' }}>السنة الثالثة ابتدائي</option>
                            <option value="4th Year of Primary School" {{ old('educational_level') == '4th Year of Primary School' ? 'selected' : '' }}>السنة الرابعة ابتدائي</option>
                            <option value="5th Year of Primary School" {{ old('educational_level') == '5th Year of Primary School' ? 'selected' : '' }}>السنة الخامسة ابتدائي</option>
                            <option value="6th Year of Primary School" {{ old('educational_level') == '6th Year of Primary School' ? 'selected' : '' }}>السنة السادسة ابتدائي</option>
                        </optgroup>
                        <optgroup label="الثانوي الإعدادي :">
                            <option value="1st Year of Middle School" {{ old('educational_level') == '1st Year of Middle School' ? 'selected' : '' }}>السنة الأولى إعدادي</option>
                            <option value="2nd Year of Middle School" {{ old('educational_level') == '2nd Year of Middle School' ? 'selected' : '' }}>السنة الثانية إعدادي</option>
                            <option value="3rd Year of Middle School" {{ old('educational_level') == '3rd Year of Middle School' ? 'selected' : '' }}>السنة الثالثة إعدادي</option>
                        </optgroup>
                        <optgroup label="الثانوي الثأهيلي :">
                            <option value="Common Core" {{ old('educational_level') == 'Common Core' ? 'selected' : '' }}>المشترك العلمي</option>
                            <option value="1st Year of Baccalaureate" {{ old('educational_level') == '1st Year of Baccalaureate' ? 'selected' : '' }}>السنة الأولى من البكالوريا</option>
                            <option value="2nd Year of Baccalaureate" {{ old('educational_level') == '2nd Year of Baccalaureate' ? 'selected' : '' }}>السنة الثانية من البكالوريا</option>
                        </optgroup>
                        <optgroup label="التعليم العالي">
                            <option value="Post-Baccalaureate" {{ old('educational_level') == 'Post-Baccalaureate' ? 'selected' : '' }}>الدراسة بعد البكالوريا</option>
                        </optgroup><option value="Post-Baccalaureate" {{ old('educational_level') == 'Post-Baccalaureate' ? 'selected' : '' }}>الدراسة بعد البكالوريا</option>
                    </select>
                    
                    @error('educational_level')
                        <small class="text-danger">{{ $message }}</small>
                    @enderror                  
            </div>

            <hr>
                <div class="form">
                    <label class="label">
                        </i><i class="fas fa-book"></i> صنف الفيديو  :
                    </label>
            
                        <select class="form-control form-select @error('the_type') is-invalid @enderror" name="the_type">
                            <option value="" disabled selected>اختر صنف الفيديو :</option>
                            <option value='أديان' {{ old('the_type') == 'أديان' ? 'selected' : '' }}>التربية الإسلامية</option>
                            <option value='فلسفة' {{ old('the_type') == 'فلسفة' ? 'selected' : '' }}>فلسفة</option>

                            <optgroup label="اللغات">
                                <option value="الأمازيغية" {{ old('the_type') == 'الأمازيغية' ? 'selected' : '' }}>الأمازيغية</option>
                                <option value="العربية" {{ old('the_type') == 'العربية' ? 'selected' : '' }}>تعلم العربية</option>
                                <option value="الفرنسية" {{ old('the_type') == 'الفرنسية' ? 'selected' : '' }}>الفرنسية</option>
                                <option value="الإنجليزية" {{ old('the_type') == 'الإنجليزية' ? 'selected' : '' }}>الإنجليزية</option>
                            </optgroup>
                            <hr>
                            <optgroup label="العلوم">
                                <option value="رياضيات" {{ old('the_type') == 'رياضيات' ? 'selected' : '' }}> رياضيات</option>
                                <option value="الكيمياء" {{ old('the_type') == 'الكيمياء' ? 'selected' : '' }}> كيمياء</option>
                                <option value="الفزياء" {{ old('the_type') == 'الفزياء' ? 'selected' : '' }}>الفزياء </option>
                                <option value="علوم الحياة والأرض" {{ old('the_type') == 'علوم الحياة والأرض' ? 'selected' : '' }}>علوم الحياة والأرض</option>
                            </optgroup>
                            <hr>
                            <optgroup label="مواضيع أخرى">
                                <option value="صحة وحياة" {{ old('the_type') == 'صحة وحياة' ? 'selected' : '' }}>صحة وحياة</option>
                                <option value="علوم الحاسوب" {{ old('the_type') == 'علوم الحاسوب' ? 'selected' : '' }}>علوم الحاسوب</option>
                                <option value="حقوق الإنسان" {{ old('the_type') == 'حقوق الإنسان' ? 'selected' : '' }}>القانون وحقوق الإنسان</option>
                                <option value="الثقافة العامة" {{ old('the_type') == 'الثقافة العامة' ? 'selected' : '' }}>الثقافة العامة</option>
                                <option value="أصناف أخرى" {{ old('the_type') == 'أصناف أخرى' ? 'selected' : '' }}>أصناف أخرى</option>
                            </optgroup>
                        </select>
                    </div>
                    @error('the_type')
                    <div class="error-feedback">
                        <i class="fas fa-exclamation-circle"></i> {{ $message }}
                    </div>
                    @enderror
                </div>
            <hr>
                
            <div class="form-row form">
                <label class="label">
                    <i class="fas fa-hourglass-start"></i>  يجب أن يكون عمر الزائر:
                </label>                
                <div class="form-group">
                    <label for="min_age" class="form-label">أكبر من:</label>
                    <div class="col-4">
                        <input 
                            value="{{ old('min_age')}}"
                            type="number" 
                            id="min_age" 
                            class="form-control" 
                            name="min_age" 
                            placeholder="الحد الأدنى" 
                            min="2" 
                            max="75"
                        >
                    </div>
                    @error('min_age')
                    <div class="error-feedback">
                        <i class="fas fa-exclamation-circle"></i> {{ $message }}
                    </div>
                    @enderror
                </div>

                <div class="form-group">
                    <label for="max_age" class="form-label">وأصغر من:</label>
                    <div class="col-4">
                        <input 
                            value="{{ old('max_age')}}"
                            type="number" 
                            id="max_age" 
                            class="form-control" 
                            name="max_age" 
                            placeholder="الحد الأقصى" 
                            min="2" 
                            max="75"
                        >
                    </div>
                    @error('max_age')
                    <div class="error-feedback">
                        <i class="fas fa-exclamation-circle"></i> {{ $message }}
                    </div>
                    @enderror
                </div>
            </div>

            <hr>

            <div class="form">
                <label class="label">
                    <i class="fas fa-info-circle"></i> وصف لمحتوى الفيديو سيظهر في محركات البحث ومواقع أخرى :
                </label><br>
                <textarea
                    name="Mydescription" 
                    placeholder="أكتب وصفًا وجيزا لمحتوى الفيديو يشجع على مشاهدته..."
                    class="form-control textarea-container"
                >{{ old('Mydescription') }}</textarea>
                @error('Mydescription')
                    <small class="text-danger">{{ $message }}</small>
                @enderror
            </div>

            <hr>

            <div class="form">
                <label class="label">
                    <i class="fas fa-key"></i> الكلمات المفتاحية:
                </label><br>
                <textarea
                    name="keywords" 
                    placeholder="الكلمات المفتاحية ..."
                    class="form-control textarea-container"
                >{{ old('keywords') }}</textarea>
                @error('keywords')
                    <small class="text-danger">{{ $message }}</small>
                @enderror
            </div>

            <button class="add_btn btn btn-primary" type="submit">
                <i class="fas fa-paper-plane"></i> نشر الفيديو
            </button>
        </form>
    </article>
</section>
        

<script>
    document.getElementById('video_url').addEventListener('input', function() {
    var videoUrl = this.value.trim();
    var videoPreview = document.getElementById('videoPreview');

    var fileFormatRegex = /^[\wÀ-ž\s-]+\.(mp4|mp3|avi|mkv|mov|flv|wmv)$/i;

    if (fileFormatRegex.test(videoUrl)) {
        videoPreview.innerHTML = `<p style="color:green;">تم إدخال ملف فيديو: ${videoUrl}</p>`;
        return; // إنهاء العملية هنا دون محاولة تحويل الرابط
    }

    var youtubeRegex = /(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:watch\?v=|embed\/|v\/)|youtu\.be\/)([\w\-]+)/;
    var match = videoUrl.match(youtubeRegex);

    if (match) {
        var videoId = match[1];
        var iframe = `<iframe width="560" height="315" src="https://www.youtube.com/embed/${videoId}" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>`;
        videoPreview.innerHTML = iframe;
    } else {
        videoPreview.innerHTML = '<p style="color:red;">الرابط غير صالح. يرجى إدخال رابط يوتيوب صحيح أو اسم ملف فيديو صالح.</p>';
    }
});


        
    document.getElementById('formFile').addEventListener('change', function(event) {
        const file = event.target.files[0];
        const preview = document.getElementById('imagePreview');

        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                preview.src = e.target.result;
                preview.style.display = 'block';
            }
            reader.readAsDataURL(file);
        } else {
            preview.src = '';
            preview.style.display = 'none';
        }
    });

        document.getElementById('video_url').addEventListener('input', function () {
            var url = this.value;
    
        var invalidYouTubeRegex = /^(https?:\/\/)?(www\.)?youtube\.com\/watch\?v=([^&]+)&?/;
        
        if (invalidYouTubeRegex.test(url)) {
            var videoId = url.match(invalidYouTubeRegex)[3];
            var validUrl = "https://www.youtube.com/embed/" + videoId;
            
            this.value = validUrl;
        }
    });
</script>

</x-layoutAdm>