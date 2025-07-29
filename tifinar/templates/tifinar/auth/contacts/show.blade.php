<x-layoutAdm page="عرض معلومات : {{ $contact->Prenom }} {{ $contact->Nom }}">
    <article class="content">
        <h1 class="mb-4"><i class="fas fa-user"></i> عرض معلومات : {{ $contact->Prenom }} {{ $contact->Nom }}</h1>
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

        <div class="card mb-4">
            <div class="card-body">
                <h5 class="card-title"><i class="fas fa-id-badge"></i> الرقم التسلسلي: {{ $contact->contacts_id }}</h5>
                <hr>
                <p class="card-text"><i class="fas fa-user"></i> <strong>الإسم الشخصي:</strong> {{ $contact->Prenom }}</p>
                <hr>
                <p class="card-text"><i class="fas fa-users"></i> <strong>الإسم العائلي:</strong> {{ $contact->Nom }}</p>
                <hr>
                <p class="card-text"><i class="fas fa-user"></i> <strong> الإسم بالعربية:</strong> {{ $contact->name_in_arabic }}</p>
                <hr>
                <p class="card-text"><i class="fas fa-venus-mars"></i> <strong>الجنس:</strong>  
                    @if($contact->gender == 'Female')
                        أنثى
                    @elseif($contact->gender == 'Male')
                        ذكر
                    @else
                        آخر
                    @endif
                    <hr>
                </p>

                @if ( $contact->Email !='')
                    <p class="card-text"><i class="fas fa-envelope"></i> <strong>البريد الإلكتروني:</strong> {{ $contact->Email }}</p>
                    <hr>
                @endif

                @if ( $contact->Tel !='')
                    <p class="card-text"><i class="fas fa-phone"></i> <strong>رقم الهاتف:</strong> {{ $contact->Tel }}</p>
                    <hr>
                @endif

                @if (Auth::user()->role == 'admin')
                        <p class="card-text"><i class="fas fa-list"></i> <strong>لائحة:</strong>
                            @switch($contact->the_type)
                                @case('Code') كلمة سرية @break
                                @case('collegue') زملاء العمل @break
                                @case('PDG') أصحاب الشركات @break
                                @case('Sup') رؤساء العمل @break
                                @case('Famille') العائلة @break
                                @case('Connaissances') المعارف @break
                                @case('Num.Pro') أرقام مهنية @break
                                @case('Ami (e)') الأصدقاء @break
                                @default
                                    غير معروف
                            @endswitch
                        </p>
                    <hr>
                @endif

                @if ( $contact->Societe !='')
                    <p class="card-text"><i class="fas fa-building"></i> <strong>المهنة :</strong> {{ $contact->Societe }}</p>
                    <hr>
                @endif
                
                @if ( $contact->Ville_D_origine !='')
                    <p class="card-text"><i class="fas fa-city"></i> <strong>المدينة الأصلية:</strong> {{ $contact->Ville_D_origine }}</p>
                    <hr>
                @endif

                @if ( $contact->social_media !='')
                    <p class="card-text"><i class="fas fa-share-alt"></i> <strong>وسائل التواصل الإجتماعي:</strong>
                        @php
                        $social_media_raw = explode(',', $contact->social_media);
                        $social_media = [];
                    
                        foreach ($social_media_raw as $entry) {
                            $parts = explode('=', $entry);
                            if (count($parts) === 2) {
                                $social_media[trim($parts[0])] = trim($parts[1]);
                            }
                        }
                    @endphp

                    @if ($social_media !='')
                            <style>
                                ul li::before {
                                    content: "\002B9C"; /* Insère une flèche */
                                    left: 0;
                                }
                            </style>
                        <ul>
                            @foreach ($social_media as $site => $user_name)
                            
                                <li style=" list-style: none;">
                                    <style>
                                        ul li::before {
                                            color: blue;
                                        }
                                    </style>
                                    @if ($site == 'facebook')
                                        <a href="https://www.facebook.com/{{$user_name}}" target="_blank">
                                            {{$user_name}} <i class="fab fa-facebook"></i>
                                        </a>
                                    @elseif ($site == 'youtube')
                                    <style>
                                        ul li::before {
                                            color: red;
                                        }
                                    </style>
                                        <a href="https://www.youtube.com/{{$user_name}}" target="_blank" style="color: red;">
                                            {{$user_name}} <i class="fab fa-youtube"></i>
                                        </a>
                                    @elseif ($site == 'instagram')
                                    <style>
                                        ul li::before {
                                            color: #dd2a7b;
                                        }
                                    </style>
                                        <a href="https://www.instagram.com/{{$user_name}}" style="color:#dd2a7b;" target="_blank">
                                            {{$user_name}} <i style=" padding:2px; color:white; background: linear-gradient(45deg, #f58529, #dd2a7b, #8134af, #515bd4); " class="fab fa-instagram"></i>
                                        </a>
                                    @endif
                                </li>
                            @endforeach
                        </ul>
                    @endif
                    
                    </p>
                    <hr>
                @endif

                
                <p class="card-text">💍 <strong>الحالة الإجتماعية:</strong> 

                    @switch($contact->Etat_Social)

                        @case('Celibataire') <span class="badge bg-warning"> {{ $contact->gender == 'Female' ? 'عازبة' : 'عازب' }} </span> @break

                        @case('Veu(f)ve') <span class="badge bg-danger">{{ $contact->gender == 'Female' ? 'أرملة' : 'أرمل' }} </span> @break

                        @case('Marie(e)') {{ $contact->gender == 'Female' ? 'متزوجة' : 'متزوج' }} من {{ $contact->spouse ?? '' }} @break

                        @case('Divorce(e)') {{ $contact->gender == 'Female' ? 'مطلقة' : 'مطلق' }} @break

                        @default <span class="badge bg-secondary">غير معروفة</span>
                    @endswitch
                </p>

                <hr>

                @if ( $contact->Adresse !='')
                    <p class="card-text"><i class="fas fa-map-marker-alt"></i> <strong>العنوان:</strong> {{ $contact->Adresse }}</p>
                    <hr>
                @endif

                @if ( $contact->Date_de_naissance !='')
                    <p class="card-text"><i class="fas fa-birthday-cake"></i> <strong>تاريخ الإزدياد:</strong> {{ $contact->Date_de_naissance }}</p>
                    <hr>
                @endif

                @if ( $contact->friends !='')
                    <p class="card-text"><i class="fas fa-user-friends"></i><strong> الأصدقاء:</strong> {{ $contact->friends }}</p>
                    <hr>
                @endif

                @if ( $contact->parents !='')
                    <p class="card-text"><i class="fas fa-user-friends"></i><strong> الأبوين:</strong> {{ $contact->parents }}</p>
                    <hr>
                @endif

                @if ( $contact->siblings !='')
                    <p class="card-text"><strong><i class="fas fa-users"></i>  الإخوة:</strong> {{ $contact->siblings }}</p>
                    <hr>
                @endif

                @if ( $contact->grandparents !='')
                    <p class="card-text"><i class="fas fa-people-arrows"></i> <strong> الأجداد:</strong> {{ $contact->grandparents }}</p>
                    <hr>
                @endif

                @if ( $contact->maternal_relatives !='')
                    <p class="card-text"><i class="fas fa-hand-holding-heart"></i><strong> الأقارب من جهة الأم:</strong> {{ $contact->maternal_relatives }}</p>
                    <hr>
                @endif

                @if ( $contact->parental_relatives !='')
                    <p class="card-text"><i class="fas fa-hand-holding-heart"></i><strong> الأعمام:</strong> {{ $contact->parental_relatives }}</p>
                    <hr>
                @endif

                <p class="card-text"><i class="fas fa-graduation-cap"></i> <strong>المستوي الدراسي:</strong> {{ $contact->educational_level }}</p>
                <hr>

                @if ( $contact->Ideologie !='' and  Auth::user()->role == 'admin')
                    <p class="card-text"><i class="fas fa-comment-dots"></i> <strong>الآراء الدينية والسياسية:</strong> {{ $contact->Ideologie }}</p>
                    <hr>
                @endif

                @if ( $contact->Commentaire !='')
                    <p class="card-text"><i class="fas fa-info-circle"></i> <strong>معلومات إضافية أخرى:</strong> {{ $contact->Commentaire }}</p>
                    <hr>
                @endif

            </div>
        </div>

        <div class="d-flex gap-2 mb-4">
            <a href="{{ route('contacts.edit', $contact) }}" class="btn btn-primary">
                <i class="fas fa-edit"></i> تعديل العضو
            </a>

            <div class="d-flex justify-content-between align-items-center mb-3">
                <form action="{{ route('contacts.removeUserIdFromAuthor', $contact->contacts_id) }}" method="POST">
                    @csrf
                    <button title="حذف العضو" type="submit" class="btn btn-danger btn-sm" onclick="return confirm('هل أنت متأكد من حذف هذا العضو؟');"><i class="fas fa-trash-alt"></i></button>
                </form>
                <a href="{{ url()->previous() }}" class="btn btn-outline-secondary btn-lg">
                    <i class="fas fa-arrow-left"></i> العودة
                </a>
            </div>
        </div>

        <div class="modal fade" id="deleteModal" tabindex="-1" aria-labelledby="deleteModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content border-danger">
                    <!-- الرأس -->
                    <div class="modal-header bg-danger text-white">
                        <h5 class="modal-title" id="deleteModalLabel">
                            <i class="fas fa-exclamation-triangle"></i> تأكيد الحذف
                        </h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <!-- المحتوى -->
                    <div class="modal-body text-center">
                        <p class="fs-5">
                            <i class="fas fa-question-circle text-warning"></i> 
                            هل أنت متأكد من أنك تريد حذف هذا العضو؟
                        </p>
                    </div>
                    <!-- الأزرار -->
                    <div class="modal-footer justify-content-center">
                        <button type="button" class="btn btn-outline-secondary btn-lg" data-bs-dismiss="modal">
                            <i class="fas fa-times-circle"></i> إلغاء
                        </button>
                        <form action="{{ route('contacts.removeUserIdFromAuthor', $contact->contacts_id) }}" method="POST">
                            @csrf
                            <button title="حذف العضو" type="submit" class="btn btn-danger btn-sm" onclick="return confirm('هل أنت متأكد من حذف هذا العضو؟');"><i class="fas fa-trash-alt"></i></button>
                        </form>
                    </div>
                </div>
            </div>
        </div>

    </article>
</x-layoutAdm>
