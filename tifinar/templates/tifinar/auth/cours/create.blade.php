
<x-layoutAdm page='نشر درس جديد'>
        <article class="content">
            <h1><i class="fas fa-edit"></i> نشر درس جديد</h1>

            @if (Auth::user()->role != "admin")
                <label class="label">
                    <i class="fas fa-user"></i>
                    {{ Auth::user()->Prenom .' '. Auth::user()->Nom }}
                </label>
            @endif

            <form method="POST" enctype="multipart/form-data" action="{{ route('cours.store') }}">
                @csrf

                <div class="mb-3 form">
                    <label class="label">
                        <i class="fas fa-upload"></i> تحميل صورة:
                    </label>

                    <input class="form-control" type="file" id="formFile" name="Myimage">
                    @error('Myimage')
                        <small class="text-danger">{{ $message }}</small>
                    @enderror
                    <img id="imagePreview" class="image-preview" alt="معاينة الصورة" style="display: none;">
                </div>

                <hr>

                <div class="form">
                    <label class="label">
                        <i class="fas fa-heading"></i> عنوان الدرس :
                    </label>
                    <input
                        type="text"
                        name="title"
                        placeholder="عنوان المنشور ..."
                        minlength="7"
                        class="title form-control"
                        value="{{old('title')}}"
                    >
                    @error('title')
                        <small class="text-danger">{{ $message }}</small>
                    @enderror
                </div>

                <hr>

                <div class="form">
                    <label class="label">
                        <i class="fas fa-heading"></i> نوع القاموس:
                    </label>
                    <select name="the_type" class="input">
                        <option value="with_board">على شكل أزرار وشاشة</option>
                        <option value="without_board">صور مع الأسماء</option>
                    </select>
                    @error('the_type')
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
                                maxlength="255"
                                name="Author"
                                placeholder="اسم الكاتب ..."
                                class="author form-control"
                                value="{{ old('author') ?? Auth::user()->Prenom .' '. Auth::user()->Nom }}"
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
                        <i class="fas fa-align-left"></i> مقدمة الدرس  :
                    </label>
                    <div><textarea
                        name="intro" 
                        type="text"
                        class="form-control">{{ old('intro') }}</textarea>
                    </div>
                    @error('intro')
                        <small class="text-danger">{{ $message }}</small>
                    @enderror
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

                <div class="form-group form">
                    <label class="label"><i class="fas fa-key"></i> اسم الملف الذي يضم الصور :</label>
                    <input
                        max="50"
                        name="Myfile"
                        value="{{ old('Myfile') }}"
                        placeholder="اسم الملف الذي يضم الصور...">
                    @error('Myfile')
                        <small class="text-danger">{{ $message }}</small>
                    @enderror
                </div>

                <hr>

                <div class="form">
                    <label class="label">
                        <i class="fas fa-link"></i> رفع صورة الدرس واسم الصورة:
                    </label>

                    <div id="image-fields-container">
                        <div class="image-field">
                            <input class="form-control image-file" type="file" name="images[]" accept="image/*">
                            <input class="form-control" type="text" name="image_names[]" placeholder="اسم الصورة">
                            <img class="image-preview" style="display: none; max-width: 100px; margin-top: 10px;" />
                            <br><hr>
                        </div>
                        @error('image_names.*')
                            <small class="text-danger">{{ $message }}</small>
                        @enderror
                        
                    </div>


                    <button type="button" id="add-image-field" class="btn btn-secondary mt-2">
                        إضافة صورة أخرى
                    </button>
                
                    @error('images.*')
                    <div class="alert alert-danger mt-2">{{ $message }}</div>
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
                        <i class="fas fa-key"></i> الكلمات المفتاحية :
                    </label><br>
                    <textarea
                        maxlength="255"
                        name="keywords" 
                        placeholder="الكلمات المفتاحية ..."
                        class="Keywords"
                    >{{ old('keywords') }}</textarea>
                    @error('keywords')
                        <div class="alert alert-danger mt-2">{{ $message }}</div>
                    @enderror
                </div>

                <hr>

                <div class="form">
                    <label class="label">
                        <i class="fas fa-link"></i> إذا كان هناك اختبار تريد أن يجتازه الشخص بعد نهاية الدرس ضع رابطه هنا 👇  :
                    </label>
                    <input
                        name="exams_link"
                        placeholder="حقل اختياري* : أضف رابط الاختبار فقط في حالة إذا كان هناك اختبار يجتازه الزرائر"
                        type="text"
                        class="description"
                        value="{{ old('exams_link') }}">
                    @error('exams_link')
                        <div class="alert alert-danger mt-2">{{ $message }}</div>
                    @enderror
                </div>

                <button class="add_btn btn btn-primary" type="submit">
                    <i class="fas fa-paper-plane"></i> نشر الدرس
                </button>

            </form>
        </article>
</x-layoutAdm>

<script>
document.getElementById('add-image-field').addEventListener('click', function () {
    let newField = document.createElement('div');
    newField.classList.add('image-field');

    let uniqueId = 'image-field-' + Date.now();

    let fileInput = document.createElement('input');
    fileInput.classList.add('form-control', 'image-file');
    fileInput.type = 'file';
    fileInput.name = 'images[]';
    fileInput.id = uniqueId;
    fileInput.accept = 'image/*';

    let nameInput = document.createElement('input');
    nameInput.classList.add('form-control');
    nameInput.type = 'text';
    nameInput.name = 'image_names[]';
    nameInput.placeholder = 'اسم الصورة';

    let previewImage = document.createElement('img');
    previewImage.classList.add('image-preview');
    previewImage.style.display = 'none';
    previewImage.style.maxWidth = '100px';
    previewImage.style.marginTop = '10px';

    let br = document.createElement('br');
    let hr = document.createElement('hr');

    // ترتيب العناصر داخل الحقل الجديد
    newField.appendChild(fileInput);
    newField.appendChild(nameInput);
    newField.appendChild(previewImage);
    newField.appendChild(hr);
    newField.appendChild(br);

    // إضافة الحقل الجديد إلى الحاوية
    document.getElementById('image-fields-container').appendChild(newField);

    // إضافة مستمع الحدث لمعاينة الصورة
    fileInput.addEventListener('change', function (event) {
        const file = event.target.files[0];
        const preview = newField.querySelector('.image-preview');

        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                preview.src = e.target.result;
                preview.style.display = 'block';
            };
            reader.readAsDataURL(file);
        } else {
            preview.src = '';
            preview.style.display = 'none';
        }
    });
});

    document.getElementById('image-fields-container').addEventListener('change', function (event) {
        if (event.target.classList.contains('image-file')) {
            const file = event.target.files[0];
            const preview = event.target.closest('.image-field').querySelector('.image-preview');

            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
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
