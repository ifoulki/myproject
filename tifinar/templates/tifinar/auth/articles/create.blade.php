
<x-layoutAdm page='نشر مقال جديد'>

        <article class="content">
            <h1> <i class="fas fa-edit"></i> نشر مقال جديد</h1>

            @if (Auth::user()->role != "admin")
            <label class="label">
                <i class="fas fa-user"></i>
                {{ Auth::user()->Prenom .' '. Auth::user()->Nom }}
            </label>
            
        @endif

            <form method="POST" enctype="multipart/form-data" action="{{ route('articles.store') }}">
                @csrf

                <div class="mb-3 form">
                <label class="label">
                    <i class="fas fa-upload"></i> تحميل صورة:
                </label>

                    <input class="form-control" type="file" id="formFile1" name="Myimage[]">

                    @error('Myimage')
                        <small class="text-danger">{{ $message }}</small>
                    @enderror
                </div>

                <img id="imagePreview1" class="image-preview" alt="معاينة الصورة" style="display: none;">

                <hr>

                <label class="label">
                    <i class="fas fa-heading"></i> عنوان المقال :
                </label>
                <input
                    required
                    type="text"
                    name="title"
                    placeholder="عنوان المنشور ..."
                    minlength="7"
                    class="title form-control"
                    value="{{ old('title') }}"
                >
                @error('title')
                    <small class="text-danger">{{ $message }}</small>
                @enderror
    
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
                            maxlength="50"
                            class="author form-control"
                            value="{{ old('author') ?? Auth::user()->Prenom .' '.Auth::user()->Nom }}"
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
                    @error('Author')
                        <small class="text-danger">{{ $message }}</small>
                    @enderror
                @endif

                <hr>

                <div class="form">
                    <label class="label">
                        <i class="fas fa-align-left"></i> نص المقال :
                    </label><br>
                    <textarea
                        name="Mysubject" 
                        minlength="100"
                        class="Mysubject"
                    >{{ old('Mysubject') }}</textarea>

                    @error('Mysubject')
                        <small class="text-danger">{{ $message }}</small>
                    @enderror
                </div>
    
                <div class="form">
                    <label class="label">
                        <i class="fas fa-upload"></i> تحميل صورة أخرى تظهر أسفل المقال:
                    </label>
    
                    <div class="mb-3">
                        <input class="form-control" type="file" id="formFile2" name="autre[]">

                        @error('autre')
                            <small class="text-danger">{{ $message }}</small>
                        @enderror
                    </div>
    
                    <img id="imagePreview2" class="image-preview" alt="معاينة الصورة" style="display: none;">
                </div>

                <hr>

                <div class="form">
                    <label class="label">
                        <i class="fas fa-list"></i> نوع المنشور:
                    </label>
                    <select class="form-control form-select" name="the_type">
                            <option value="" disabled selected>اختر نوع المنشور</option>
                            @foreach ([ 'الأمازيغية', 'تربية وتعليم', 'الثقافة العامة','علوم','القانون وحقوق الإنسان'] as $item)
                                <option value="{{$item}}" {{old('the_type') ? "selected":"";}} >{{ $item }}</option>
                            @endforeach
                    </select>
                </div>

                <hr>

                <div class="mb-3 form">
                    <label for="educational_level" class="form-label">
                        <i class="fas fa-graduation-cap"></i> هل يجب أن يكون للقارئ مستوى دراسي محدد لقراءة هذا المقال؟
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

                        <optgroup label="الإبتدائي :">
                            <option value="1st Year of Middle School" {{ old('educational_level') == '1st Year of Middle School' ? 'selected' : '' }}>السنة الأولى إعدادي</option>
                            <option value="2nd Year of Middle School" {{ old('educational_level') == '2nd Year of Middle School' ? 'selected' : '' }}>السنة الثانية إعدادي</option>
                            <option value="3rd Year of Middle School" {{ old('educational_level') == '3rd Year of Middle School' ? 'selected' : '' }}>السنة الثالثة إعدادي</option>
                        </optgroup>

                        <optgroup label="الإبتدائي :">
                            <option value="Common Core" {{ old('educational_level') == 'Common Core' ? 'selected' : '' }}>المشترك العلمي</option>
                            <option value="1st Year of Baccalaureate" {{ old('educational_level') == '1st Year of Baccalaureate' ? 'selected' : '' }}>السنة الأولى من البكالوريا (تخصص علوم تجريبية)</option>
                            <option value="2nd Year of Baccalaureate" {{ old('educational_level') == '2nd Year of Baccalaureate' ? 'selected' : '' }}>السنة الثانية من البكالوريا (تخصص علوم فيزيائية)</option>
                        </optgroup>

                        <optgroup label="الإبتدائي :">
                            <option value="Post-Baccalaureate" {{ old('educational_level') == 'Post-Baccalaureate' ? 'selected' : '' }}>الدراسة بعد البكالوريا</option>
                        </optgroup>

                    </select>
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
                        <i class="fas fa-info-circle"></i> وصف المنشور :
                    </label><br>
                    <textarea
                        maxlength="255"
                        name="Mydescription" 
                        placeholder="أكتب وصفًا لمنشورك ..."
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
                        name="keywords"
                        maxlength="255"
                        placeholder="الكلمات المفتاحية ..."
                        class="Keyword"
                    >{{ old('keywords') }}</textarea>
                </div>
    
                <button class="add_btn btn btn-primary" type="submit">
                    <i class="fas fa-paper-plane"></i> نشر المقال
                </button>
                
            </form>
        </article>

    <script>
        document.querySelectorAll('input[type="file"]').forEach(input => {
            input.addEventListener('change', function(event) {
                const file = event.target.files[0];
                const previewId = event.target.id.replace('formFile', 'imagePreview');
                const preview = document.getElementById(previewId);
        
                if (preview) {
                    if (file) {
                        const reader = new FileReader();
                        reader.onload = function(e) {
                            preview.src = e.target.result;
                            preview.style.display = 'block';
                        };
                        reader.readAsDataURL(file);
                    } else {
                        preview.src = '';
                        preview.style.display = 'none';
                    }
                }
            });
        });
    </script>

</x-layoutAdm>