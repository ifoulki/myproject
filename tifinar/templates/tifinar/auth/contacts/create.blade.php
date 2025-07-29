
<x-layoutAdm page='تسجيل عضو جديد'>

        <article class="content">
            <h1> <i class="fas fa-edit"></i>  تسجيل عضو جديد</h1>
            @if ($errors->any())
                <div class="alert alert-danger">
                    <ul>
                        @foreach ($errors->all() as $error)
                            <li>{{ $error }}</li>
                        @endforeach
                    </ul>
                </div>
            @endif

            <form method="POST" enctype="multipart/form-data" action="{{ route('contacts.store') }}">
                @csrf
                
                <input value="{{Auth::user()->id}}" name="Author" >
    
                <label class="label">
                    <i class="fas fa-upload"></i> تحميل صورة :
                </label>
                <div class="mb-3">
                    <input class="form-control" type="file" id="formFileMultiple" name="Myimage[]" multiple>
                    <div class="form-text">يمكنك اختيار ملفات متعددة.</div>
                </div>
    
                <hr>
                <div class="mb-3">
                    <label class="form-label"><i class="fas fa-user"></i>الإسم الشخصي :</label>
                    <input type="text" name="Prenom" class="form-control" value="{{ old('Prenom')}}">
                </div>

                <div class="mb-3">
                    <label class="form-label"><i class="fas fa-user"></i>الإسم العائلي :</label>
                    <input type="text" name="Nom" class="form-control" value="{{ old('Nom')}}">
                </div>

                <hr>

                <div>
                    <div class="mb-3">
                        <label for="educational_level" class="form-label">
                            <i class="fas fa-graduation-cap"></i>المستوى الدراسي :
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
                                <option value="2nd Year of Baccalaureate" {{ old('educational_level') == '2nd Year of Baccalaureate' ? 'selected' : '' }}>السنة الثانية من البكالوريا</option>
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

                <div class="mb-3">
                    <label class="form-label"><i class="fas fa-comment-dots"></i> الآراء الدينية والسياسية </label>
                    <textarea name="Ideologie" class="form-control" rows="3">{{ old('Ideologie') }}</textarea>
                </div>

                <div class="mb-3">
                    <label class="form-label"><i class="fas fa-info-circle"></i> معلومات إضافية أخرى :</label>
                    <textarea name="Commentaire" class="form-control" rows="3">{{ old('Commentaire') }}</textarea>
                </div>


                <div class="form-group">
                    <label for="spouse"><i class="fas fa-heart"></i>الزوج/الزوجة</label>
                    <input type="text" name="spouse" id="spouse" class="form-control" value="{{ old('spouse') }}">
                </div>

                <div class="form-group">
                    <label for="children"><i class="fas fa-baby"></i>الأبناء</label>
                    <textarea name="children" id="children" class="form-control" rows="3">{{ old('children') }}</textarea>
                </div>
                <div class="form-group">
                    <label for="siblings">
                        <i class="fas fa-users"></i> الإخوة والأخوات
                    </label>
                    <textarea name="siblings" id="siblings" class="form-control" rows="3" placeholder="أدخل أسماء الإخوة والأخوات">{{ old('siblings') }}</textarea>
                </div>
                
                <div class="form-group">
                    <label for="parents">
                        <i class="fas fa-user-friends"></i> الوالدان
                    </label>
                    <textarea name="parents" id="parents" class="form-control" rows="3" placeholder="أدخل معلومات عن الوالدين">{{ old('parents') }}</textarea>
                </div>

                <div class="form-group">
                    <label for="maternal_relatives">
                        <i class="fas fa-hand-holding-heart"></i> الأقارب من جهة الأم
                    </label>
                    <textarea name="maternal_relatives" id="maternal_relatives" class="form-control" rows="3" placeholder="أدخل أسماء أقارب جهة الأم">{{ old('maternal_relatives') }}</textarea>
                </div>

                <div class="form-group">
                    <label for="paternal_relatives">
                        <i class="fas fa-hand-holding-heart"></i> الأقارب من جهة الأب
                    </label>
                    <textarea name="paternal_relatives" id="paternal_relatives" class="form-control" rows="3" placeholder="أدخل أسماء أقارب جهة الأب">{{ old('paternal_relatives') }}</textarea>
                </div>

                <div class="form-group">
                    <label for="grandparents">
                        <i class="fas fa-people-arrows"></i> الأجداد
                    </label>
                    <textarea name="grandparents" id="grandparents" class="form-control" rows="3" placeholder="أدخل معلومات عن الأجداد">{{ old('grandparents') }}</textarea>
                </div>

                <div class="form-group">
                    <label for="friends">
                        <i class="fas fa-user-friends"></i> الأصدقاء
                    </label>
                    <textarea name="friends" id="friends" class="form-control" rows="3" placeholder="أدخل أسماء الأصدقاء">{{ old('friends') }}</textarea>
                </div>

                <div class="form-group">
                    <label for="name_in_arabic">
                        <i class="fas fa-font"></i> الاسم بالعربية
                    </label>
                    <input type="text" name="name_in_arabic" id="name_in_arabic" class="form-control" placeholder="أدخل الاسم باللغة العربية" value="{{ old('name_in_arabic') }}">
                </div>                

                <div class="mb-3">
                    <label class="form-label"><i class="fas fa-key"></i> الكلمات المفتاحية :</label>
                    <textarea name="keywords" class="form-control" rows="2">{{ old('keywords') }}</textarea>
                </div>

    
                <button class="add_btn btn btn-primary" type="submit">
                    <i class="fas fa-paper-plane"></i> نشر المقال
                </button>
                
            </form>
        </article>
    </x-layoutAdm>