
<x-layoutAdm page='نشر كتاب جديد'>

    <section>
        <article class="content">
            <h1> <i class="fas fa-video"></i> نشر كتاب جديد</h1>

            @if (Auth::user()->role != "admin")
                <label class="label">
                    <i class="fas fa-user"></i>
                    {{ Auth::user()->name }}
                </label>
            @endif

            <form method="POST" enctype="multipart/form-data" action="{{ route('videos.store') }}">
                @csrf
    
                <label class="label">
                    <i class="fas fa-upload"></i> تحميل صورة غلاف الكتاب:
                </label>
                <div class="mb-3">
                    <input class="form-control" type="file" id="formFile" name="Myimage">
                </div>

                <img id="imagePreview" class="image-preview" alt="معاينة الصورة" style="display: none;">

                <hr>
                <label class="label">
                    <i class="fas fa-heading"></i> عنوان الكتاب :
                </label>
                <input
                    required
                    type="text"
                    name="title"
                    placeholder="عنوان الكتاب ..."
                    minlength="7"
                    class="title form-control"
                    value="{{ old('title') }}"
                >
    
                <hr>
    
                <div>
                    @if (Auth::user()->role == "admin")
                        <label class="label">
                            <i class="fas fa-user"></i> اسم الكاتب:
                        </label>
                        <input 
                            type="text" 
                            name="Author"
                            placeholder="اسم الكاتب ..."
                            minlength="5"
                            class="author form-control"
                            value="{{ Auth::user()->name }}"
                        />
                    @endif
                </div>
    
                <hr>
    
                <div>
                    <label class="label">
                        <i class="fas fa-align-left"></i> عما يتحدث الكتاب؟ أكتب موجز قصير يشجع على تحميله :
                    </label><br>
                    <textarea
                        required
                        name="Mysubject" 
                        class="Mysubject"
                    >{{ old('Mysubject') }}</textarea>
                </div>
    
                <div>
                    <label class="label">
                        <i class="fas fa-paperclip"></i>  اسم وصيغة الكتاب  :
                    </label><br>
                    <input
                        name="autre" 
                        class="Mysubject"
                        placeholder="مثل : book.pdf, book.ppt ... ect"
                        value="{{ old('autre') }}"
                    >
                </div>
    
                <hr>
                <div>
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
                            <option value="رياضيات" {{ old('the_type') == 'رياضيات' ? 'selected' : '' }}>تعلم الرياضيات</option>
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
                </div>
    
                <hr>
    
                <div>
                    <label class="label">
                        <i class="fas fa-info-circle"></i> وصف لمحتوى الكتاب :
                    </label><br>
                    <textarea
                        required 
                        name="Mydescription" 
                        placeholder="أكتب وصفًا يشجع للدخول للصفحة ..."
                        class="description"
                    >{{ old('Mydescription') }}</textarea>
                </div>
    
                <hr>
    
                <div>
                    <label class="label">
                        <i class="fas fa-key"></i> الكلمات المفتاحية :
                    </label><br>
                    <textarea
                        name="Keyword" 
                        placeholder="الكلمات المفتاحية ..."
                        class="Keyword"
                    >{{ old('Keyword') }}</textarea>
                </div>
    
                <button class="add_btn btn btn-primary" type="submit">
                    <i class="fas fa-paper-plane"></i> نشر الكتاب
                </button>
                
            </form>
        </article>
    </section>
    
    <script>
        document.getElementById('formFile').addEventListener('change', function(event) {
            const file = event.target.files[0];
            const preview = document.getElementById('imagePreview');

            if (file) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                    preview.src = e.target.result;
                    preview.style.display = 'block'; // إظهار الصورة
                }
                reader.readAsDataURL(file);
            } else {
                preview.src = '';
               preview.style.display = 'none'; // إخفاء الصورة
            }
        });
    </script>

</x-layoutAdm>