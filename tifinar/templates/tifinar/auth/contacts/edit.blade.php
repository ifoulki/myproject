<x-layoutAdm page="تعديل معلومات : {{ $contact->Prenom }} {{ $contact->Nom }}">

        <article class="content">

            <h1 class="mb-4">تعديل معلومات : {{ $contact->Prenom }} {{ $contact->Nom }}</h1>
            @if ($errors->any())
                <div class="alert alert-danger">
                    <ul>
                        @foreach ($errors->all() as $error)
                            <li>{{ $error }}</li>
                        @endforeach
                    </ul>
                </div>
            @endif

            @php
            $images=explode(',',$contact->path);
            shuffle($images);
        @endphp
        
        @if($contact->path!='') 
        @php 
            $images = explode(',', $contact->path);
        @endphp
            <div id="imageCarousel" class="carousel slide mb-4" data-bs-ride="carousel">
                <div class="carousel-inner">
                    @foreach($images as $index => $image)
                        <div class="carousel-item {{ $index === 0 ? 'active' : '' }}">
                            <img src="{{ asset('images/contacts/' . $image ) }}" class="d-block w-100" alt="photo de {{ $contact->Prenom }} {{ $contact->Nom }}" style="max-width:400px; margin: auto;">
                        </div>
                    @endforeach
                </div>
                <button class="carousel-control-prev" type="button" data-bs-target="#imageCarousel" data-bs-slide="prev">
                    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">السابق</span>
                </button>
                <button class="carousel-control-next" type="button" data-bs-target="#imageCarousel" data-bs-slide="next">
                    <span class="carousel-control-next-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">التالي</span>
                </button>
            </div>
        @else
            @if ($contact->gender =='Male')
                <div class="text-center mb-4">
                    <img src="{{ asset('assets/male.webp') }}" class="img-fluid" alt="photo de {{ $contact->Prenom }} {{ $contact->Nom}}" style="max-width:400px;">
                </div>
            @else
                <div class="text-center mb-4">
                    <img src="{{ asset('assets/female.webp') }}" class="img-fluid" alt="photo de {{ $contact->Prenom }} {{ $contact->Nom}}" style="max-width:400px;">
                </div>
            @endif
        @endif

            <form method="post" action="{{ route('contacts.update', $contact) }}" enctype="multipart/form-data">
                @csrf
                @method('PUT')

                <input type="hidden" value="{{Auth::user()->name}}" name="Author">

                <div class="mb-3">
                    <label class="form-label"><i class="fas fa-id-card"></i>رقم العضو :</label>
                    <input type="number" name="contacts_id" class="form-control" value="{{ $contact->contacts_id   }}">
                </div>

                <div class="mb-3">
                    <label class="form-label"><i class="fas fa-user"></i>الإسم الشخصي :</label>
                    <input type="text" name="Prenom" class="form-control" value="{{ $contact->Prenom   }}">
                </div>

                <div class="mb-3">
                    <label class="form-label"><i class="fas fa-user"></i>الإسم العائلي :</label>
                    <input type="text" name="Nom" class="form-control" value="{{ $contact->Nom   }}">
                </div>

                <div class="form-group">
                    <label for="name_in_arabic">
                        <i class="fas fa-font"></i> الاسم بالعربية
                    </label>
                    <input type="text" name="name_in_arabic" id="name_in_arabic" class="form-control" placeholder="أدخل الاسم باللغة العربية" value="{{ $contact->name_in_arabic }}">
                </div>

                <div class="mb-3">
                    <label for="gender" class="form-label">
                        <i class="fas fa-venus-mars"></i> الجندر:
                    </label>
                    <select id="gender" name="gender" class="form-select">
                        <option value="Male" {{ $contact->gender == 'Male' ? 'selected' : '' }}>
                            ♂️ ذكر
                        </option>
                        <option value="Female" {{ $contact->gender == 'Female' ? 'selected' : '' }}>
                            ♀️ أنثى
                        </option>
                        <option value="Other" {{ $contact->gender == 'Other' ? 'selected' : '' }}>
                            <i class="fas fa-transgender-alt"></i> آخر
                        </option>
                        <option value="Unknown" {{ $contact->gender == 'Unknown' ? 'selected' : '' }}>
                            غير معروف
                        </option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="Date_de_naissance"><i class="fas fa-birthday-cake"></i> تاريخ الازدياد :</label>
                    <input type="date" name="Date_de_naissance" id="Date_de_naissance" class="form-control" value="{{ $contact->Date_de_naissance}}">
                </div>

                <div class="mb-3">
                    <label for="the_type" class="form-label"><i class="fas fa-list"></i>لائحة:</label>
                    <select id="the_type" name="the_type" class="form-select">
                        <option value="Code" {{ $contact->the_type   == 'Code' ? 'selected' : '' }}>كلمة سرية</option>
                        <option value="collegue" {{ $contact->the_type   == 'collegue' ? 'selected' : '' }}>زملاء العمل</option>
                        <option value="inconnu" {{ $contact->the_type   == 'inconnu' ? 'selected' : '' }}>غير معروف</option>
                        <option value="Sup" {{ $contact->the_type   == 'Sup' ? 'selected' : '' }}>رئيس في العمل</option>
                        <option value="Famille" {{ $contact->the_type   == 'Famille' ? 'selected' : '' }}>العائلة</option>
                        <option value="Connaissances" {{ $contact->the_type   == 'Connaissances' ? 'selected' : '' }}>المعارف</option>
                        <option value="Num.Pro" {{ $contact->the_type   == 'Num.Pro' ? 'selected' : '' }}>رقم مهني</option>
                        <option value="Ami (e)" {{ $contact->the_type   == 'Ami (e)' ? 'selected' : '' }}>الأصدقاء</option>
                        <option value="PDG" {{ $contact->the_type   == 'PDG' ? 'selected' : '' }}>صاحب شركة</option>
                    </select>
                </div>

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

                <div class="form-group">
                    <label for="Societe"><i class="fas fa-building"></i>الشركة :</label>
                    <input type="text" name="Societe" id="Societe" class="form-control" value="{{ $contact->Societe}}">
                </div>

                <div class="form-group">
                    <label for="Ville_D_origine"><i class="fas fa-city"></i>المذينة الأصلية :</label>
                    <input type="text" name="Ville_D_origine" id="Ville_D_origine" class="form-control" value="{{ $contact->Ville_D_origine}}">
                </div>

                <div class="form-group">
                    <label for="social_media">وسائل التواصل الاجتماعي</label>
                    <textarea name="social_media" id="social_media" class="form-control" rows="3">{{ $contact->social_media }}</textarea>
                </div>

                <div class="form-group">
                    <label for="Adresse"><i class="fas fa-map-marker-alt"></i> العنوان</label>
                    <input type="text" name="Adresse" id="Adresse" class="form-control" value="{{ $contact->Adresse}}">
                </div>

                <div class="mb-3">
                    <label for="Etat_Social" class="form-label">💍 الحالة الاجتماعية:</label>
                    <select id="Etat_Social" name="Etat_Social" class="form-select">
                        <option value="Celibataire" {{ $contact->Etat_Social   == 'Celibataire' ? 'selected' : '' }}>عازب(ة)</option>
                        <option value="Marie(e)" {{ $contact->Etat_Social   == 'Marie(e)' ? 'selected' : '' }}>متزوج(ة)</option>
                        <option value="Fiancee" {{ $contact->Etat_Social   == 'Fiancee' ? 'selected' : '' }}>مخطوبة</option>
                        <option value="Veu(f)ve" {{ $contact->Etat_Social   == 'Veu(f)ve' ? 'selected' : '' }}>أرمل(ة)</option>
                        <option value="Divorce(e)" {{ $contact->Etat_Social   == 'Divorce(e)' ? 'selected' : '' }}>مطلق(ة)</option>
                        <option value="Organisme" {{ $contact->Etat_Social   == 'Organisme' ? 'selected' : '' }}>مؤسسة</option>
                        <option value="Unknown" {{ $contact->Etat_Social   == 'Unknown' ? 'selected' : '' }}>غير معروفة</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="spouse"><i class="fas fa-heart"></i>الزوج/الزوجة</label>
                    <input type="text" name="spouse" id="spouse" class="form-control" value="{{ $contact->spouse}}">
                </div>

                
                <div class="form-group">
                    <label for="children"><i class="fas fa-baby"></i>الأبناء</label>
                    <textarea name="children" id="children" class="form-control" rows="3">{{ $contact->children}}</textarea>
                </div>

                <div class="form-group">
                    <label for="siblings">
                        <i class="fas fa-users"></i> الإخوة والأخوات
                    </label>
                    <textarea name="siblings" id="siblings" class="form-control" rows="3" placeholder="أدخل أسماء الإخوة والأخوات">{{ $contact->siblings }}</textarea>
                </div>
                
                <div class="form-group">
                    <label for="parents">
                        <i class="fas fa-user-friends"></i> الوالدان
                    </label>
                    <textarea name="parents" id="parents" class="form-control" rows="3" placeholder="أدخل معلومات عن الوالدين">{{ $contact->parents }}</textarea>
                </div>

                <div class="form-group">
                    <label for="maternal_relatives">
                        <i class="fas fa-hand-holding-heart"></i> الأقارب من جهة الأم
                    </label>
                    <textarea name="maternal_relatives" id="maternal_relatives" class="form-control" rows="3" placeholder="أدخل أسماء أقارب جهة الأم">{{ $contact->maternal_relatives }}</textarea>
                </div>

                <div class="form-group">
                    <label for="paternal_relatives">
                        <i class="fas fa-hand-holding-heart"></i> الأقارب من جهة الأب
                    </label>
                    <textarea name="paternal_relatives" id="paternal_relatives" class="form-control" rows="3" placeholder="أدخل أسماء أقارب جهة الأب">{{ $contact->paternal_relatives }}</textarea>
                </div>

                <div class="form-group">
                    <label for="grandparents">
                        <i class="fas fa-people-arrows"></i> الأجداد
                    </label>
                    <textarea name="grandparents" id="grandparents" class="form-control" rows="3" placeholder="أدخل معلومات عن الأجداد">{{ $contact->grandparents }}</textarea>
                </div>

                <div class="form-group">
                    <label for="friends">
                        <i class="fas fa-user-friends"></i> الأصدقاء
                    </label>
                    <textarea name="friends" id="friends" class="form-control" rows="3" placeholder="أدخل أسماء الأصدقاء">{{ $contact->friends }}</textarea>
                </div>

                <div class="mb-3">
                    <label class="form-label"><i class="fas fa-comment-dots"></i> الآراء الدينية والسياسية </label>
                    <textarea name="Ideologie" class="form-control" rows="3">{{ $contact->Ideologie  }}</textarea>
                </div>

                <div class="mb-3">
                    <label class="form-label"><i class="fas fa-info-circle"></i> معلومات إضافية أخرى :</label>
                    <textarea name="Commentaire" class="form-control" rows="3">{{ $contact->Commentaire  }}</textarea>
                </div>

                <div class="mb-3">
                    <label class="form-label"><i class="fas fa-key"></i> الكلمات المفتاحية :</label>
                    <textarea name="keywords" class="form-control" rows="2">{{ $contact->keywords  }}</textarea>
                </div>

                <div class="d-flex justify-content-between">
                    <button type="submit" name="eddit_mbr" class="btn btn-primary">
                        <i class="fas fa-edit"></i> تعديل العضو
                    </button>
                    
                    <form action="{{ route('contacts.removeUserIdFromAuthor', $contact->contacts_id) }}" method="POST">
                        @csrf
                        <button title="حذف العضو" type="submit" class="btn btn-danger btn-sm" onclick="return confirm('هل أنت متأكد من حذف هذا العضو؟');"><i class="fas fa-trash-alt"></i></button>
                    </form>
                </div>
            </form>
        </article>
</x-layoutAdm>

