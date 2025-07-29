
<x-layoutAdm page='إنشاء اختبار جديد'>

    <article class="form content">

        <h1><i class="fas fa-edit"></i> إنشاء اختبار جديد:</h1>
            @if (Auth::user()->role != "admin")
                <label class="label">
                    <i class="fas fa-user"></i>
                    {{ Auth::user()->Prenom .' '. Auth::user()->Nom }}
                </label>
            @endif

        <form class="form" method="POST" action="{{ route('exams.store') }}" enctype="multipart/form-data">

            @csrf
            <div class="form">
                <label class="label">
                    <i class="fas fa-upload"></i> تحميل صورة:
                </label>
                <input class="form-control @error('Myimage') is-invalid @enderror" type="file" id="formFile" name="Myimage" accept="image/*">
                <div id="preview-container" style="margin-top: 10px;">
                    <img id="preview-image" src="#" alt="معاينة الصورة" style="max-width: 100%; max-height: 200px; display: none;"/>
                </div>
                @error('the_type')
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
                    <i class="fas fa-heading"></i> عنوان الاختبار :
                </label>
                <input 
                    type="text" 
                    maxlength="200"
                    name="title" 
                    placeholder="موضوع الاختبار ..." 
                    class="input @error('title') is-invalid @enderror" 
                    value="{{ old('title') }}"
                >
                @error('title')
                        <small class="text-danger">{{ $message }}</small>
                @enderror
            </div>
    
            <hr>
    
            <div class="form">
                <label class="label">
                    <i class="fas fa-language"></i> بأي لغة ستطرح السؤال؟
                </label>
                <select class="form-control form-select @error('dir') is-invalid @enderror" name="dir">
                    <option value="" disabled selected>اختر نوع المنشور</option>
                    <option value="rtl" {{ old('dir') === 'rtl' ? 'selected' : '' }}>العربية</option>
                    <option value="ltr" {{ old('dir') === 'ltr' ? 'selected' : '' }}>Français</option>
                    <option value="ltr" {{ old('dir') === 'ltr' ? 'selected' : '' }}>English</option>
                </select>
                @error('the_type')
                        <small class="text-danger">{{ $message }}</small>
                @enderror
            </div>
            <hr>
    
            <div class="form">
                <label class="label">
                    </i><i class="fas fa-book"></i> موضوع الاختبار :
                </label>
        
                    <select class="form-control form-select @error('the_type') is-invalid @enderror" name="the_type">
                        <option value="" disabled selected>اختر موضوع الاختبار</option>
                        <optgroup label="اللغات">
                            <option value="الأمازيغية" {{ old('the_type') == 'الأمازيغية' ? 'selected' : '' }}>الأمازيغية</option>
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
                        <small class="text-danger">{{ $message }}</small>
                @enderror
            </div>

            <hr>

            <div class="mb-3 form">
                <label for="educational_level" class="form-label"><i class="fas fa-graduation-cap"></i> هل الاختبار خاص بمستوى دراسي محدد؟:</label>
                    <select id="educational_level" name="educational_level" class="form-select">
                            <option value="Unknown" {{ old('educational_level') == 'Unknown' ? 'selected' : '' }}>لا، الاختبار مناسب للجميع</option>
                            <option value="Preschool" {{ old('educational_level') == 'Preschool' ? 'selected' : '' }}>للأطفال الصغار، أقل من 6 سنوات</option>
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
                            <option value="3rd Year of Middle School" {{ old('educational_level') == '3rd Year of Middle School' ? 'selected' : '' }}>السنة الثالثة إعدادي </option>
                        </optgroup>
                        <optgroup label="الثانوي الثأهيلي :">
                            <option value="Common Core" {{ old('educational_level') == 'Common Core' ? 'selected' : '' }}>المشترك العلمي</option>
                            <option value="1st Year of Baccalaureate" {{ old('educational_level') == '1st Year of Baccalaureate' ? 'selected' : '' }}>السنة الأولى بكالوريا</option>
                            <option value="2nd Year of Baccalaureate" {{ old('educational_level') == '2nd Year of Baccalaureate' ? 'selected' : '' }}>السنة الثانية بكالوريا</option>
                        </optgroup>
                        <optgroup label="التعليم العالي">
                            <option value="Post-Baccalaureate" {{ old('educational_level') == 'Post-Baccalaureate' ? 'selected' : '' }}>الدراسة بعد البكالوريا</option>
                        </optgroup>
                    </select>
                @error('educational_level')
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
                    <i class="fas fa-heading"></i> وصف الاختبار :
                </label>
                <textarea
                    type="text" 
                    maxlength="255"
                    name="Mydescription" 
                    placeholder=" أكتب وصف موجز لهذا الاختبار ..." 
                    class="@error('Mydescription') is-invalid @enderror" 
                >{{ old('Mydescription') }}</textarea>
                @error('the_type')
                        <small class="text-danger">{{ $message }}</small>
                @enderror
            </div>

            <div class="form">
                <label class="label">
                    <i class="fas fa-heading"></i> الكلمات المفتاحية :
                </label>
                <textarea
                    type="text" 
                    maxlength="255"
                    name="keywords" 
                    placeholder=" أكتب الكلمات المفتاحية ..." 
                    class="@error('keywords') is-invalid @enderror" 
                >{{ old('keywords') }}</textarea>
                @error('keywords')
                    <small class="text-danger">{{ $message }}</small>
                @enderror
            </div>

            <div class="text-center">
                <button type="submit" class="btn btn-success">
                    <i class="fas fa-plus"></i> حفظ المعلومات وإضافة الأسئلة
                </button>
            </div>
        </form>
    </article>
    

    <script>
    
        document.getElementById('formFile').addEventListener('change', function(event) {
            const previewImage = document.getElementById('preview-image');
            const file = event.target.files[0];
        
            if (file) {
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    previewImage.src = e.target.result;
                    previewImage.style.display = 'block'; // إظهار الصورة
                };
        
                reader.readAsDataURL(file);
            } else {
                previewImage.src = "#";
                previewImage.style.display = 'none'; // إخفاء الصورة
            }
        });
        </script>
    
    </x-layoutAdm>