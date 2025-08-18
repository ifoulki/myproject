<x-layoutAdm page="تعديل معلومات : {{ $User->Prenom }} {{ $User->Nom }}">
    <style>
        .gender-container {
            display: flex;
            gap: 20px;
            align-items: center;
        }

        .gender-container label {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 16px;
            cursor: pointer;
        }

        .gender-container input[type="radio"] {
            margin: 0;
        }
    </style>

    @if (session('error'))
        <div class="alert alert-danger">
            {{ session('error') }}
        </div>
    @endif

    @if (session('success'))
        <div class="alert alert-success">
            {{ session('success') }}
        </div>
    @endif


    <article class="content">

        <h1 class="mb-4">تعديل معلومات : {{ $User->Prenom }} {{ $User->Nom }}</h1>

        <form class="form" action="{{ route('auth.users.update', $User->id) }}" method="POST" enctype="multipart/form-data">

            @csrf
            @method('PUT')

            @php
                $images = explode(',', $User->path);
                shuffle($images);
            @endphp

            <div class="mb-3 text-center">
                <img id="imagePreview" class="img-fluid mb-2" alt="معاينة الصورة"
                    style="display: none; max-width: 400px;">
                @if (!empty($images[0]))
                    <img id="currentImage" src="{{ asset($images[0]) }}" alt="الصورة الحالية" class="img-fluid mb-2"
                        style="max-width: 400px;">
                @else
                    <img id="currentImage"
                        src="{{ asset('assets/' . ($User->gender === 'Male' ? 'male.webp' : 'female.webp')) }}"
                        alt="صورة {{ $User->Prenom }} {{ $User->Nom }}" class="img-fluid mb-2"
                        style="max-width: 400px;">
                @endif
            </div>

            <div class="mb-3">
                <label for="formFile" class="form-label d-block">
                    <i class="fas fa-upload"></i> تعديل الصورة الشخصية:
                </label>
                <input class="form-control" type="file" id="formFile" name="path" accept="image/*">
                @error('path')
                    <small class="text-danger">{{ $message }}</small>
                @enderror
            </div>
            <button type="submit" name="eddit_mbr" class="btn btn-primary">
                <i class="fas fa-edit"></i> حفظ الصورة الشخصية
            </button>
        </form>

        <hr>

        <form class="form" action="{{ route('auth.users.update', $User->id) }}" method="POST" enctype="multipart/form-data">
            @csrf
            @method('PUT')
            <h1>
                <i class="fas fa-user"></i> تعديل الإسم ومعلومات التواصل:
            </h1>
            <div class="mb-3">
                <label class="form-label"><i class="fas fa-user"></i>الإسم الشخصي :</label>
                <input type="text" name="Prenom" class="form-control input" value="{{ $User->Prenom }}">
                @error('Prenom')
                    <small class="text-danger">{{ $message }}</small>
                @enderror
            </div>

            <hr>

            <div class="mb-3">
                <label class="form-label"><i class="fas fa-user"></i>الإسم العائلي :</label>
                <input type="text" name="Nom" class="form-control input" value="{{ $User->Nom }}">
                @error('Nom')
                    <small class="text-danger">{{ $message }}</small>
                @enderror
            </div>

            <hr>

            <div class="mb-3">
                <label for="name_in_arabic">
                    <i class="fas fa-font"></i> الاسم الكامل بالعربية
                </label>
                <input type="text" name="name_in_arabic" id="name_in_arabic" class="form-control input"
                    placeholder="أدخل الاسم الكامل باللغة العربية"
                    value="{{ old('name_in_arabic', $User->name_in_arabic ?? '') }}">
                @error('name_in_arabic')
                    <small class="text-danger">{{ $message }}</small>
                @enderror
            </div>

            <hr>

            <div class="mb-3">
                <i class="fas fa-font"></i>الجندر : <br>
                <div class="mb-3 position-relative gender-container">
                    <label class="form-label">
                        <input type="radio" value="Male" name="gender"
                            {{ (old('gender') ?? $User->gender) == 'Male' ? 'checked' : '' }}>
                        ذكر ♂️
                    </label>
                    <label class="form-label">
                        <input type="radio" value="Female" name="gender"
                            {{ (old('gender') ?? $User->gender) == 'Female' ? 'checked' : '' }}>
                        أنثى ♀️
                    </label>
                    <label class="form-label">
                        <input type="radio" value="Other" name="gender"
                            {{ (old('gender') ?? $User->gender) == 'Other' ? 'checked' : '' }}>
                        آخر <i class="fas fa-transgender-alt"></i>
                    </label>
                </div>
            </div>

            <hr>


            <div class="mb-3">
                <label for="Tel" class="form-label"><i class="fas fa-phone"></i> رقم الهاتف :</label>
                <input type="text" name="Tel" id="Tel" class="form-control input" value="{{ $User->Tel }}">
            </div>

            <hr>

            <div class="mb-3">
                <label for="email" class="form-label"><i class="fas fa-list"></i> البريد الالكتروني :</label>
                <input type="text" name="email" id="email" class="form-control input" value="{{ $User->email }}">
                @error('email')
                    <small class="text-danger">{{ $message }}</small>
                @enderror
            </div>

            <hr>

            <div class="mb-3">
                <label for="Ville_D_origine"><i class="fas fa-city"></i>المذينة الأصلية :</label>
                <input type="text" name="Ville_D_origine" id="Ville_D_origine" class="form-control input" value="{{ old('Ville_D_origine', $User->Ville_D_origine) }}">
            </div>

            <hr>

            <div class="mb-3">
                <label for="Adresse"><i class="fas fa-map-marker-alt"></i> العنوان</label>
                <input type="text" name="Adresse" id="Adresse" class="form-control input" value="{{ old('Adresse', $User->Adresse) }}">
            </div>

            <hr>

            <div class="mb-3">
                <h4>وسائل التواصل الاجتماعي</h4>

                    <label for="social_media_1"> الفيسبوك Facebook : </label>
                    <input type="text" id="social_media_1" name="social_media_1" value="{{ old('social_media_1', explode(',', $User->social_media)[0] ?? '') }}">
                
                    <label for="social_media_2"> يوتيوب Youtube :</label>
                    <input type="text" id="social_media_2" name="social_media_2" value="{{ old('social_media_2', explode(',', $User->social_media)[1] ?? '') }}">
                
                    <label for="social_media_3">أنستغرام Instagram :</label>
                    <input type="text" id="social_media_3" name="social_media_3" value="{{ old('social_media_3', explode(',', $User->social_media)[2] ?? '') }}">
                
                    <label for="social_media_4">سناب شات Snapchat :</label>
                    <input type="text" id="social_media_4" name="social_media_4" value="{{ old('social_media_4', explode(',', $User->social_media)[3] ?? '') }}">
                
                    <input type="hidden" id="social_media" name="social_media" value="{{ $User->social_media }}">

                <script>
                    const form = document.querySelector('form');
                    form.addEventListener('submit', function(e) {
                        const socialMedia = [
                            document.getElementById('social_media_1').value,
                            document.getElementById('social_media_2').value,
                            document.getElementById('social_media_3').value,
                            document.getElementById('social_media_4').value
                        ].filter(Boolean).join(',');
                        document.getElementById('social_media').value = socialMedia;
                    });
                </script>
                
            </div>

            <button type="submit" name="eddit_mbr" class="btn btn-primary">
                <i class="fas fa-edit"></i> حفظ الإسم ومعلومات التواصل
            </button>
        </form>

        <hr>

        
        <form class="form" action="{{ route('auth.users.update', $User->id) }}" method="POST" enctype="multipart/form-data">
            @csrf
            @method('PUT')

            <h1>
                <i class="fas fa-briefcase"></i> الدراسة والعمل:
            </h1>

            <div class="mb-3">
                <label for="Societe"><i class="fas fa-building"></i>المهنة :</label>
                <input type="text" name="Societe" id="Societe" class="form-control" value="{{ $User->Societe }}">
            </div>

            <hr>

            <div class="mb-3">
                <label for="educational_level" class="form-label"><i class="fas fa-graduation-cap"></i> المستوي
                    الدراسي:</label>
                <select id="educational_level" name="educational_level" class="form-select form-control">
                        <option value="" disabled selected>حدد المستوى الدراسي</option>
                        
                        <option value="Preschool"
                            {{ (old('educational_level') ?? $User->educational_level) == 'Preschool' ? 'selected' : '' }}>
                            روضة الأطفال</option>
                        <option value="Unknown"
                            {{ (old('educational_level') ?? $User->educational_level) == 'Unknown' ? 'selected' : '' }}>
                            غير متعلم في المدرسة</option>
                    <optgroup label="التعليم الابتدائي">
                        <option value="1st Year of Primary School"
                            {{ (old('educational_level') ?? $User->educational_level) == '1st Year of Primary School' ? 'selected' : '' }}>
                            السنة الأولى ابتدائي</option>
                        <option value="2nd Year of Primary School"
                            {{ (old('educational_level') ?? $User->educational_level) == '2nd Year of Primary School' ? 'selected' : '' }}>
                            السنة الثانية ابتدائي</option>
                        <option value="3rd Year of Primary School"
                            {{ (old('educational_level') ?? $User->educational_level) == '3rd Year of Primary School' ? 'selected' : '' }}>
                            السنة الثالثة ابتدائي</option>
                        <option value="4th Year of Primary School"
                            {{ (old('educational_level') ?? $User->educational_level) == '4th Year of Primary School' ? 'selected' : '' }}>
                            السنة الرابعة ابتدائي</option>
                        <option value="5th Year of Primary School"
                            {{ (old('educational_level') ?? $User->educational_level) == '5th Year of Primary School' ? 'selected' : '' }}>
                            السنة الخامسة ابتدائي</option>
                        <option value="6th Year of Primary School"
                            {{ (old('educational_level') ?? $User->educational_level) == '6th Year of Primary School' ? 'selected' : '' }}>
                            السنة السادسة ابتدائي</option>
                    </optgroup>

                    <optgroup label="التعليم الإعدادي">    
                        <option value="1st Year of Middle School"
                            {{ (old('educational_level') ?? $User->educational_level) == '1st Year of Middle School' ? 'selected' : '' }}>
                            السنة الأولى إعدادي</option>
                        <option value="2nd Year of Middle School"
                            {{ (old('educational_level') ?? $User->educational_level) == '2nd Year of Middle School' ? 'selected' : '' }}>
                            السنة الثانية إعدادي</option>
                        <option value="3rd Year of Middle School"
                            {{ (old('educational_level') ?? $User->educational_level) == '3rd Year of Middle School' ? 'selected' : '' }}>
                            السنة الثالثة إعدادي</option>
                    </optgroup>
                    <optgroup label="التعليم الثانوي">
                        <option value="Common Core"
                            {{ (old('educational_level') ?? $User->educational_level) == 'Common Core' ? 'selected' : '' }}>
                            جدع مشترك</option>
                        <option value="1st Year of Baccalaureate"
                            {{ (old('educational_level') ?? $User->educational_level) == '1st Year of Baccalaureate' ? 'selected' : '' }}>
                            السنة الأولى بكالوريا</option>
                        <option value="2nd Year of Baccalaureate"
                            {{ (old('educational_level') ?? $User->educational_level) == '2nd Year of Baccalaureate' ? 'selected' : '' }}>
                            السنة الثانية بكالوريا</option>
                    </optgroup>
                    
                    <optgroup label="التعليم العالي">
                        <option value="Post-Baccalaureate"
                        {{ (old('educational_level') ?? $User->educational_level) == 'Post-Baccalaureate' ? 'selected' : '' }}>
                        التعليم العالي</option>
                    </optgroup>
                    
                </select>
            </div>
            <button type="submit" name="eddit_mbr" class="btn btn-primary">
                <i class="fas fa-edit"></i> حفظ معلومات الدراسة والعمل
            </button>
        </form>

        <hr>

        @if (Auth::user()?->role == 'admin')
            <div class="mb-3">
                <label for="role" class="form-label"><i class="fas fa-list"></i>الدور :</label>
                <select id="role" name="role" class="form-select form-control">
                    <option value="" disabled selected>اختر دور العضو</option>
                    <option value="admin" {{ (old('role') ?? $User->role) == 'admin' ? 'selected' : '' }}>مدير
                        الموقع</option>
                    <option value="content_creator"
                        {{ (old('role') ?? $User->role) == 'content_creator' ? 'selected' : '' }}>منشئ محتوى</option>
                    <option value="user" {{ (old('role') ?? $User->role) == 'user' ? 'selected' : '' }}>مستخدم
                        للموقع</option>
                </select>
            </div>
        @endif

        <hr>

        <form class="form" action="{{ route('auth.users.update', $User->id) }}" method="POST" enctype="multipart/form-data">
            @csrf
            @method('PUT')

            <h1>
                <i class="fas fa-user"></i> معلومات شخصية أخرى:
            </h1>

            <div class="mb-3">
                <label for="Date_de_naissance"><i class="fas fa-birthday-cake"></i> تاريخ الازدياد :</label>
                <input type="date" name="Date_de_naissance" id="Date_de_naissance" class="form-control"
                    value="{{ $User->Date_de_naissance }}">
            </div>

            <hr>

            <div class="mb-3">
                <label for="Etat_Social" class="form-label">💍 الحالة الاجتماعية:</label>
                <select id="Etat_Social" name="Etat_Social" class="form-select form-control">
                    <option value="" disabled {{ old('Etat_Social') == '' ? 'selected' : '' }}>حدد الحالة
                        الاجتماعية</option>
                    <option value="Celibataire"
                        {{ (old('Etat_Social') ?? $User->Etat_Social) == 'Celibataire' ? 'selected' : '' }}>
                        عازب(ة)
                    </option>
                    <option value="Marie(e)"
                        {{ (old('Etat_Social') ?? $User->Etat_Social) == 'Marie(e)' ? 'selected' : '' }}>
                        متزوج(ة)
                    </option>
                    <option value="Fiancee"
                        {{ (old('Etat_Social') ?? $User->Etat_Social) == 'Fiancee' ? 'selected' : '' }}>
                        مخطوبة
                    </option>
                    <option value="Veu(f)ve"
                        {{ (old('Etat_Social') ?? $User->Etat_Social) == 'Veu(f)ve' ? 'selected' : '' }}>
                        أرمل(ة)
                    </option>
                    <option value="Divorce(e)"
                        {{ (old('Etat_Social') ?? $User->Etat_Social) == 'Divorce(e)' ? 'selected' : '' }}>
                        مطلق(ة)
                    </option>
                </select>
            </div>

            <hr>

            <div class="mb-3">
                <label class="form-label"><i class="fas fa-comment-dots"></i> الآراء الدينية والسياسية </label>
                <textarea name="Ideologie" class="form-control" rows="3">{{ old('Ideologie', $User->Ideologie) }}</textarea>
            </div>

            <hr>

            <div class="mb-3">
                <label class="form-label"><i class="fas fa-info-circle"></i> نبذة موجزة عنك :</label>
                <textarea name="Commentaire" class="form-control" rows="3">{{ old('Commentaire', $User->Commentaire) }}</textarea>
            </div>

            <button type="submit" name="eddit_mbr" class="btn btn-primary">
                <i class="fas fa-edit"></i> حفظ معلومات المعلومات الشخصية
            </button>
        </form>

        @if (Auth::user()?->role == 'admin')
            <form class="form" action="{{ route('auth.users.update', $User->id) }}" method="POST" enctype="multipart/form-data">

                @csrf
                @method('PUT')

                <div class="mb-3">
                    <label for="children"><i class="fas fa-baby"></i>الأبناء</label>
                    <textarea name="children" id="children" class="form-control" rows="3">{{ old('children', $User->children) }}</textarea>
                </div>

                <div class="mb-3">
                    <label for="siblings">
                        <i class="fas fa-users"></i> الإخوة والأخوات
                    </label>
                    <textarea name="siblings" id="siblings" class="form-control" rows="3"
                        placeholder="أدخل أسماء الإخوة والأخوات">{{ old('siblings', $User->siblings) }}</textarea>
                </div>

                <div class="mb-3">
                    <label for="cousin">
                        <i class="fas fa-users"></i> الإخوة والأخوات
                    </label>
                    <textarea name="cousin" id="cousin" class="form-control" rows="3"
                        placeholder="أدخل أسماء الإخوة والأخوات">{{ old('cousin', $User->cousin) }}</textarea>
                </div>

                <div class="mb-3">
                    <label for="parents">
                        <i class="fas fa-user-friends"></i> الوالدان
                    </label>
                    <textarea name="parents" id="parents" class="form-control" rows="3" placeholder="أدخل معلومات عن الوالدين">{{ old('parents', $User->parents) }}</textarea>
                </div>

                <div class="mb-3">
                    <label for="maternal_relatives">
                        <i class="fas fa-hand-holding-heart"></i> الأقارب من جهة الأم
                    </label>
                    <textarea name="maternal_relatives" id="maternal_relatives" class="form-control" rows="3"
                        placeholder="أدخل أسماء أقارب جهة الأم">{{ old('maternal_relatives', $User->maternal_relatives) }}</textarea>
                </div>

                <div class="mb-3">
                    <label for="paternal_relatives">
                        <i class="fas fa-hand-holding-heart"></i> الأقارب من جهة الأب
                    </label>
                    <textarea name="paternal_relatives" id="paternal_relatives" class="form-control" rows="3"
                        placeholder="أدخل أسماء أقارب جهة الأب">{{ old('paternal_relatives', $User->paternal_relatives) }}</textarea>
                </div>

                <div class="mb-3">
                    <label for="grandparents">
                        <i class="fas fa-people-arrows"></i> الأجداد
                    </label>
                    <textarea name="grandparents" id="grandparents" class="form-control" rows="3"
                        placeholder="أدخل معلومات عن الأجداد">{{ old('grandparents', $User->grandparents) }}</textarea>
                </div>


                <div class="mb-3">
                    <label class="form-label"><i class="fas fa-key"></i> الكلمات المفتاحية :</label>
                    <textarea name="keywords" class="form-control" rows="2">{{ old('keywords', $User->keywords) }}</textarea>
                </div>

                <div class="mb-3">
                    <label for="spouse"><i class="fas fa-heart"></i>الزوج/الزوجة</label>
                    <input type="text" name="spouse" id="spouse" class="form-control"
                        value="{{ old('spouse', $User->spouse) }}">
                </div>
                
                <div class="d-flex justify-content-between">
                    <button type="submit" name="eddit_mbr" class="btn btn-primary">
                        <i class="fas fa-edit"></i> حفظ العضو
                    </button>
                    
                    <button id="deleteBtn" class="btn btn-danger">حذف العضو</button>
                    
                    <div id="confirmationModal" class="modal">
                        <div class="modal-content">
                            <span class="closeBtn">&times;</span>
                            <p>هل أنت متأكد من أنك تريد حذف هذا العضو؟</p>
                            <button id="confirmDelete" class="btn btn-danger">نعم، احذف</button>
                            <button id="cancelDelete" class="btn btn-secondary">إلغاء</button>
                        </div>
                    </div>
                </div>
            </form>
        @endif
    </article>


    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const fileInput = document.getElementById('formFile');
            const imagePreview = document.getElementById('imagePreview');
            const currentImage = document.getElementById('currentImage');

            fileInput.addEventListener('change', (event) => {
                const file = event.target.files[0];

                if (file) {
                    const reader = new FileReader();
                    reader.onload = (e) => {
                        currentImage.style.display = 'none';
                        imagePreview.src = e.target.result;
                        imagePreview.style.display = 'block'; 
                    };
                    reader.readAsDataURL(file);
                } else {
                    imagePreview.src = '';
                    imagePreview.style.display = 'none';
                    currentImage.style.display = 'block';
                }
            });
        });
    </script>
</x-layoutAdm>
