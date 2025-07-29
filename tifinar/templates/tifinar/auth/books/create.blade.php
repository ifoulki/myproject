
<x-layoutAdm page='نشر كتاب جديد'>

        <article class="content">
            <h1> <i class="fas fa-video"></i> نشر كتاب جديد</h1>

            @if (Auth::user()->role != "admin")
                <label class="label">
                    <i class="fas fa-user"></i>
                    {{Auth::user()->Prenom.' '.Auth::user()->Nom}}
                </label>
            @endif

            <form method="POST" enctype="multipart/form-data" action="{{ route('books.store') }}">
                @csrf
    
                <div class="form">
                    <label class="label">
                        <i class="fas fa-upload"></i> تحميل صورة غلاف الكتاب:
                    </label>
                    <div class="mb-3">
                        <input class="form-control" type="file" id="formFile" name="Myimage">
                        @error('Myimage')
                            <small class="text-danger">{{ $message }}</small>
                        @enderror
                    </div>

                    <img id="imagePreview" class="image-preview" alt="معاينة الصورة" style="display: none;">
                </div>

                <hr>

                <div class="form">
                    <label class="label">
                        <i class="fas fa-heading"></i> عنوان الكتاب :
                    </label>
                    <input
                        type="text"
                        name="title"
                        placeholder="عنوان الكتاب ..."
                        minlength="7"
                        class="title form-control"
                        value="{{ old('title') }}"
                    >
                    @error('title')
                        <small class="text-danger">{{ $message }}</small>
                    @enderror
                </div>

                <hr>

                <div class="form">
                    @if (Auth::user()->role == "admin")
                        <div>
                            <label class="label">
                                <i class="fas fa-user"></i> اسم الكاتب :
                            </label>
                            <input 
                                type="text" 
                                name="Author"
                                placeholder="اسم الكاتب ..."
                                maxlength="50"
                                class="author form-control"
                                value="{{ old('author') ?? Auth::user()->Prenom.' '.Auth::user()->Nom }}"
                            />
                        </div>
                    @else 
                        <input 
                            type="hidden" 
                            name="Author"
                            placeholder="اسم الكاتب ..."
                            class="author form-control"
                            value="{{ Auth::user()->Prenom .' '. Auth::user()->Nom }}"
                        />
                    @endif
                    @error('Author')
                        <small class="text-danger">{{ $message }}</small>
                    @enderror
                </div>
    
                <hr>
    
                <div class="form">
                    <label class="label">
                        <i class="fas fa-align-left"></i> عما يتحدث الكتاب؟ أكتب موجز قصير يشجع على تحميله :
                    </label><br>
                    <textarea
                        name="Mysubject" 
                        class="Mysubject"
                    >{{ old('Mysubject') }}</textarea>
                    @error('Mysubject')
                        <small class="text-danger">{{ $message }}</small>
                    @enderror
                </div>

                <hr>

                <div class="form">
                    <label class="label"><i class="fas fa-language"></i>  موجز الكتاب مكتوب بأي لغة ؟ </label>
                    <select class="small-input @error('dir') is-invalid @enderror" name="dir">
                        <option value="" disabled selected>اختر اللغة</option>
                        <option value="rtl" {{ old('dir') === 'rtl' ? 'selected' : '' }}>العربية</option>
                        <option value="ltr" {{ old('dir') === 'ltr' ? 'selected' : '' }} selected >Français</option>
                        <option value="ltr" {{ old('dir') === 'ltr' ? 'selected' : '' }}>English</option>
                    </select>
                    @error('dir')
                            <small class="text-danger">{{ $message }}</small>
                    @enderror
                </div>

                <hr>
    
                <div class="form">
                    <label class="label">
                        <i class="fas fa-upload"></i> تحميل الكتاب:
                    </label>
    
                    <div class="mb-3">
                        <input class="form-control" type="file" id="formFile" name="autre">
                        @error('autre')
                            <small class="text-danger">{{ $message }}</small>
                        @enderror
                    </div>
                </div>
    
                <hr>

                <div class="form">
                    <label class="label">
                        <i class="fas fa-list"></i> صنف الكتاب:
                    </label>
                    <select class="form-control form-select" name="the_type">
                        <option value="" disabled selected>اختر صنف الكتب</option>

                        <optgroup label="الأدب :">
                            <option value='قصص و روايات' {{ old('the_type') == 'قصص و روايات' ? 'selected' : '' }}>قصص و روايات</option>
                            <option value='قصائد شعرية' {{ old('the_type') == 'قصائد شعرية' ? 'selected' : '' }}>قصائد شعرية</option>
                            <option value='مجلات' {{ old('the_type') == 'مجلات' ? 'selected' : '' }}>مجلات</option>
                            <option value='لقواميس اللغوية - Dictionaries' {{ old('the_type') == 'لقواميس اللغوية - Dictionaries' ? 'selected' : '' }}>لقواميس اللغوية - Dictionaries</option>
                            <option value='أديان' {{ old('the_type') == 'أديان' ? 'selected' : '' }}>أديان</option>
                            <option value='فلسفة' {{ old('the_type') == 'فلسفة' ? 'selected' : '' }}>فلسفة</option>
                        </optgroup>
                        <hr>
                        <optgroup label="اللغات">
                            <option value="الأمازيغية" {{ old('the_type') == 'الأمازيغية' ? 'selected' : '' }}>تعلم الأمازيغية</option>
                            <option value="الفرنسية" {{ old('the_type') == 'الفرنسية' ? 'selected' : '' }}>تعلم الفرنسية</option>
                            <option value="الإنجليزية" {{ old('the_type') == 'الإنجليزية' ? 'selected' : '' }}>تعلم الإنجليزية</option>
                        </optgroup>
                        <hr>
                        <optgroup label="العلوم">
                            <option value="رياضيات" {{ old('the_type') == 'رياضيات' ? 'selected' : '' }} selected >تعلم الرياضيات</option>
                            <option value="الكيمياء" {{ old('the_type') == 'الكيمياء' ? 'selected' : '' }}> الكيمياء</option>
                            <option value="الفزياء" {{ old('the_type') == 'الفزياء' ? 'selected' : '' }}>الفزياء</option>
                            <option value="علوم الحياة والأرض" {{ old('the_type') == 'علوم الحياة والأرض' ? 'selected' : '' }}>علوم الحياة والأرض</option>
                        </optgroup>
                        <hr>
                        <optgroup label="مواضيع أخرى">
                            <option value="صحة وحياة" {{ old('the_type') == 'صحة وحياة' ? 'selected' : '' }}>صحة وحياة</option>
                            <option value="علوم الحاسوب" {{ old('the_type') == 'علوم الحاسوب' ? 'selected' : '' }}>علوم الحاسوب</option>
                            <option value="حقوق الإنسان" {{ old('the_type') == 'وحقوق الإنسان' ? 'selected' : '' }}>القانون وحقوق الإنسان</option>
                            <option value="الثقافة العامة" {{ old('the_type') == 'الثقافة العامة' ? 'selected' : '' }}>الثقافة العامة</option>
                            <option value="تربية وتعليم" {{ old('the_type') == 'تربية وتعليم' ? 'selected' : '' }}>تربية وتعليم</option>
                            <option value="أصناف أخرى" {{ old('the_type') == 'أصناف أخرى' ? 'selected' : '' }}>أصناف أخرى</option>
                        </optgroup>
                    </select>
                    @error('the_type')
                        <small class="text-danger">{{ $message }}</small>
                    @enderror
                </div>

                <hr>

                <div class="form">
                    <div class="mb-3">
                        <label for="educational_level" class="form-label">
                            <i class="fas fa-graduation-cap"></i>هل يجب أن يكون للقراء مستوى دراسي محدد؟
                        </label>
                        
                        <select id="educational_level" name="educational_level" class="form-select">
                                <option value="Unknown" {{ old('educational_level') == 'Unknown' ? 'selected' : '' }}>لا، الكتاب مناسب للجميع</option>
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
                                <option value="2nd Year of Baccalaureate" {{ old('educational_level') == '2nd Year of Baccalaureate' ? 'selected' : '' }} selected >السنة الثانية من البكالوريا</option>
                            </optgroup>
                            <optgroup label="التعليم العالي">
                                <option value="Post-Baccalaureate" {{ old('educational_level') == 'Post-Baccalaureate' ? 'selected' : '' }}>الدراسة بعد البكالوريا</option>
                            </optgroup>
                        </select>
                        
                    </div>
                    @error('education_level')
                        <small class="text-danger">{{ $message }}</small>
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
                        <i class="fas fa-info-circle"></i> وصف لمحتوى الكتاب :
                    </label><br>
                    <textarea
                        name="Mydescription" 
                        maxlength="255"
                        placeholder="أكتب وصفًا يشجع للدخول للصفحة ..."
                        class="description"
                    >{{ old('Mydescription') }}</textarea>
                    @error('Mydescription')
                        <small class="text-danger">{{ $message }}</small>
                    @enderror
                </div>
    
                <hr>
    
                <div class="form">
                    <label class="label">
                        <i class="fas fa-key"></i> الكلمات المفتاحية :
                    </label><br>
                    <textarea
                        maxlength="255"
                        name="keywords" 
                        placeholder="الكلمات المفتاحية ..."
                        class="keywords"
                    >{{ old('keywords') }}</textarea>
                    @error('keywords')
                        <small class="text-danger">{{ $message }}</small>
                    @enderror
                </div>
    
                <button class="add_btn btn btn-primary" type="submit">
                    <i class="fas fa-paper-plane"></i> نشر الكتاب
                </button>
                
            </form>
        </article>
    
    <script>
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
    </script>

</x-layoutAdm>
