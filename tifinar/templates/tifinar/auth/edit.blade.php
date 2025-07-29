<x-layout page='تعديل المعلومات الشخصية'>
    <section class="content">
        <div class="container">
            <h2>تعديل بيانات المستخدم</h2>
            <form method="POST" action="{{ route('user.update', $user) }}" enctype="multipart/form-data">
                @csrf
                @method('PUT')

                @php 
                    $images = explode(',', $user->images);
                    $lastImage = $images[0] ?? null;
                @endphp

            
                <div class="mb-3">
                    <label for="profile_image" class="form-label">الصورة الشخصية (اختياري)</label>

                    @if($lastImage)
                        <img id="currentImage" src="{{ asset('images/users/'.$lastImage) }}" alt="الصورة الحالية" width="100" class="mb-2">
                    @else
                        <p>لا توجد صورة حالياً</p>
                    @endif

                    <input type="file" name="profile_image[]" id="profile_image" class="form-control" multiple onchange="previewImage(event)">

                    <div id="imagePreview" class="mt-3"></div>
                    
                    @error('profile_image')
                        <small class="text-danger">{{ $message }}</small>
                    @enderror
                    
                    <script>
                        function previewImage(event) {
                            var reader = new FileReader();
                            reader.onload = function() {
                                var output = document.createElement('img');
                                output.src = reader.result;
                                output.width = 100;
                                var preview = document.getElementById('imagePreview');
                                preview.innerHTML = '';
                                preview.appendChild(output);

                                var currentImage = document.getElementById('currentImage');
                                if (currentImage) {
                                    currentImage.style.display = 'none';
                                }
                            };
                            reader.readAsDataURL(event.target.files[0]);
                        }
                    </script>
                    


                <div class="mb-3">
                    <label for="name" class="form-label">اسم المستخدم</label>
                    <input type="text" name="name" id="name" class="form-control"
                        value="{{ old('name', $user->name) }}" >
                    @error('name')
                        <small class="text-danger">{{ $message }}</small>
                    @enderror
                </div>

                <div class="mb-3">
                    <label for="educational_level" class="form-label">
                        <i class="fas fa-graduation-cap"></i> المستوى التعليمي
                    </label>
                    <select class="form-control" name="educational_level" id="educational_level" >
                        <option value="" disabled selected>اختر مستواك التعليمي</option>

                        <optgroup label="المستويات غير المدرسية">
                            <option value="Illiterate Person">غير متعلم في المدرسة</option>
                            <option value="Preschool">روضة الأطفال</option>
                        </optgroup>

                        <optgroup label="التعليم الابتدائي">
                            <option value="1st Year of Primary School" {{ $user->educational_level == '1st Year of Primary School' ? 'selected' : '' }}>السنة الأولى ابتدائي</option>
                            <option value="2nd Year of Primary School" {{ $user->educational_level == '2nd Year of Primary School' ? 'selected' : '' }}>السنة الثانية ابتدائي</option>
                            <option value="3rd Year of Primary School" {{ $user->educational_level == '3rd Year of Primary School' ? 'selected' : '' }}>السنة الثالثة ابتدائي</option>
                            <option value="4th Year of Primary School" {{ $user->educational_level == '4th Year of Primary School' ? 'selected' : '' }}>السنة الرابعة ابتدائي</option>
                            <option value="5th Year of Primary School" {{ $user->educational_level == '5th Year of Primary School' ? 'selected' : '' }}>السنة الخامسة ابتدائي</option>
                            <option value="6th Year of Primary School" {{ $user->educational_level == '6th Year of Primary School' ? 'selected' : '' }}>السنة السادسة ابتدائي</option>
                        </optgroup>

                        <optgroup label="التعليم الإعدادي">
                            <option value="1st Year of Middle School" {{ $user->educational_level == '1st Year of Middle School' ? 'selected' : '' }}>السنة الأولى إعدادي</option>
                            <option value="2nd Year of Middle School" {{ $user->educational_level == '2nd Year of Middle School' ? 'selected' : '' }}>السنة الثانية إعدادي</option>
                            <option value="3rd Year of Middle School" {{ $user->educational_level == '3rd Year of Middle School' ? 'selected' : '' }}>السنة الثالثة إعدادي</option>
                        </optgroup>

                        <optgroup label="التعليم الثانوي">
                            <option value="Common Core" {{ $user->educational_level == 'Common Core' ? 'selected' : '' }}>المسلك المشترك</option>
                            <option value="1st Year of Baccalaureate" {{ $user->educational_level == '1st Year of Baccalaureate' ? 'selected' : '' }}>السنة الأولى بكالوريا</option>
                            <option value="2nd Year of Baccalaureate" {{ $user->educational_level == '2nd Year of Baccalaureate' ? 'selected' : '' }}>السنة الثانية بكالوريا</option>
                        </optgroup>

                        <optgroup label="التعليم العالي">
                            <option value="Post-Baccalaureate" {{ $user->educational_level == 'Post-Baccalaureate' ? 'selected' : '' }}>التعليم العالي</option>
                        </optgroup>
                    </select>
                </div>
                

                @error('educational_level')
                    <small class="text-danger">{{ $message }}</small>
                @enderror

                <div class="mb-3">
                    <label for="email" class="form-label">البريد الإلكتروني</label>
                    <input type="email" name="email" id="email" class="form-control"
                        value="{{ old('email', $user->email) }}" >
                    @error('email')
                        <small class="text-danger">{{ $message }}</small>
                    @enderror
                </div>

                <div class="mb-3">
                    <label for="password" class="form-label">كلمة المرور الجديدة (اختياري)</label>
                    <input type="password" name="password" id="password" class="form-control">
                    @error('password')
                        <small class="text-danger">{{ $message }}</small>
                    @enderror
                </div>

                <div class="mb-3">
                    <label for="password_confirmation" class="form-label">تأكيد كلمة المرور الجديدة</label>
                    <input type="password" name="password_confirmation" id="password_confirmation" class="form-control">
                </div>

                <button type="submit" class="btn btn-primary">حفظ التعديلات</button>
            </form>
        </div>
    </section>
</x-layout>
