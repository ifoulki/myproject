<x-layoutAdm page="عرض معلومات : {{ $User->Prenom }} {{ $User->Nom }}">
    <article class="content">
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
        $images = explode(',', $User->path);
        shuffle($images);
    @endphp
    
    @if($User->path != '')
        <div id="imageCarousel" class="carousel slide mb-4" data-bs-ride="carousel">
            <div class="carousel-inner">
                @foreach($images as $index => $image)
                    <div class="carousel-item {{ $index === 0 ? 'active' : '' }}">
                        <img src="{{ asset($image) }}" class="d-block w-100" alt="photo de {{ $User->Prenom }} {{ $User->Nom }}" style="max-width:400px; margin: auto;">
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
        @if ($User->gender == 'Male')
            <div class="text-center mb-4">
                <img src="{{ asset('assets/male.webp') }}" class="img-fluid" alt="photo de {{ $User->Prenom }} {{ $User->Nom }}" style="max-width:400px;">
            </div>
        @else
            <div class="text-center mb-4">
                <img src="{{ asset('assets/female.webp') }}" class="img-fluid" alt="photo de {{ $User->Prenom }} {{ $User->Nom }}" style="max-width:400px;">
            </div>
        @endif
    @endif    

        <div class="card mb-4">
            <div class="card-body">
                <h1 class="mb-4"><i class="fas fa-user"></i> {{ $User->Prenom }} {{ $User->Nom }}</h1>

                @if (Auth::user()->role=="admin")
                    <h5 class="card-title"><i class="fas fa-id-badge"></i> الرقم التسلسلي: {{ $User->id }}</h5>
                    <hr>
                @endif

                <p class="card-text"><i class="fas fa-venus-mars"></i> <strong>الجنس:</strong>  
                    @if($User->gender == 'Female')
                        أنثى
                    @elseif($User->gender == 'Male')
                        ذكر
                    @else
                        آخر
                    @endif
                    <hr>
                </p>

                @if ( $User->Email !='')
                    <p class="card-text"><i class="fas fa-envelope"></i> <strong>البريد الإلكتروني:</strong> {{ $User->Email }}</p>
                    <hr>
                @endif

                @if (($User->Tel != '') && (Auth::user()->role == "admin" || Auth::user()->id == $User->id))
                    <p class="card-text"><i class="fas fa-phone"></i> <strong>رقم الهاتف:</strong> {{ $User->Tel }}</p>
                    <hr>
                @endif

                @if ( $User->role !='' and  Auth::user()->role=="admin" or Auth::user()->id== $User->id)
                    <p class="card-text"><i class="fas fa-list"></i> <strong>الصفة:</strong>
                    @switch($User->role)
                        @case('admin')
                            مدير الموقع 
                            @break
                        @case('content_creator')
                            منشئ محتوى
                            @break
                        @default
                            مستخدم للموقع
                    @endswitch
                    <hr>
                @endif

                </p>

                @if ( $User->Societe !='')
                    <p class="card-text"><i class="fas fa-building"></i> <strong>الشركة:</strong> {{ $User->Societe }}</p>
                    <hr>
                @endif

                @if ( $User->Adresse !='')
                    <p class="card-text"><i class="fas fa-map-marker-alt"></i> <strong>العنوان:</strong> {{ $User->Adresse }}</p>
                    <hr>
                @endif
                
                @if ( $User->Ville_D_origine !='')
                    <p class="card-text"><i class="fas fa-city"></i> <strong>المدينة الأصلية:</strong> {{ $User->Ville_D_origine }}</p>
                    <hr>
                @endif

                @if ( $User->social_media !='')
                    <p class="card-text"><i class="fas fa-share-alt"></i> <strong>وسائل التواصل الإجتماعي:</strong>
                        @php
                        $social_media_raw = explode(',', $User->social_media); 
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
                    @switch($User->Etat_Social)
                        @case('Celibataire')
                            @if ( $User->gender =='Female')
                                <span class="badge bg-warning">عازبة</span>
                            @else
                                <span class="badge bg-warning">عازب</span>
                            @endif

                            @break
                        @case('Veu(f)ve')
                            @if ( $User->gender =='Female')
                                <span class="badge bg-danger">أرملة</span>
                            @else
                                <span class="badge bg-danger">أرمل</span>
                            @endif

                            @break
                        @case('Organisme')
                            <span class="badge bg-info">مؤسسة</span>
                            @break
                        @case('Marie(e)')
                            @if ( $User->gender =='Female')
                                متزوجة
                            @else
                                متزوج
                            @endif

                            @if ( $User->spouse !='')
                                من  {{$User->spouse}}
                            @endif

                            @break
                        @case('Fiancee')
                            <span class="badge bg-primary">في فترة خطوبة</span>
                            @break
                        @case('Divorce(e)')
                            @if ( $User->gender =='Female')
                                <span class="badge bg-dark">مطلقة</span>
                            @else
                                <span class="badge bg-dark">مطلق</span>
                            @endif

                            @break
                        @default
                            <span class="badge bg-secondary">غير معروفة</span>
                    @endswitch
                    <hr>
                </p>

                

                @if ( $User->Date_de_naissance !='')
                    <p class="card-text"><i class="fas fa-birthday-cake"></i> <strong>تاريخ الإزدياد:</strong> {{ $User->Date_de_naissance }}</p>
                    <hr>
                @endif

                {{-- @if ( $User->friends !='')
                    <p class="card-text"><i class="fas fa-user-friends"></i><strong> الأصدقاء:</strong> {{ $User->friends }}</p>
                    <hr>
                @endif

                @if ( $User->parents !='')
                    <p class="card-text"><i class="fas fa-user-friends"></i><strong> الأبوين:</strong> {{ $User->parents }}</p>
                    <hr>
                @endif

                @if ( $User->siblings !='')
                    <p class="card-text"><strong><i class="fas fa-users"></i>  الإخوة:</strong> {{ $User->siblings }}</p>
                    <hr>
                @endif

                @if ( $User->grandparents !='')
                    <p class="card-text"><i class="fas fa-people-arrows"></i> <strong> الأجداد:</strong> {{ $User->grandparents }}</p>
                    <hr>
                @endif

                @if ( $User->maternal_relatives !='')
                    <p class="card-text"><i class="fas fa-hand-holding-heart"></i><strong> الأقارب من جهة الأم:</strong> {{ $User->maternal_relatives }}</p>
                    <hr>
                @endif

                @if ( $User->parental_relatives !='')
                    <p class="card-text"><i class="fas fa-hand-holding-heart"></i><strong> الأعمام:</strong> {{ $User->parental_relatives }}</p>
                    <hr>
                @endif --}}

                <p class="card-text"><i class="fas fa-graduation-cap"></i> <strong>المستوي الدراسي:</strong> {{ $User->educational_level }}</p>
                <hr>

                @if ( $User->Ideologie !='')
                    <p class="card-text"><i class="fas fa-comment-dots"></i> <strong>الآراء الدينية والسياسية:</strong> {{ $User->Ideologie }}</p>
                    <hr>
                @endif

                @if ( $User->Commentaire !='')
                    <p class="card-text"><i class="fas fa-info-circle"></i> <strong>معلومات إضافية أخرى:</strong> {{ $User->Commentaire }}</p>
                    <hr>
                @endif

            </div>
        </div>

        <div class="d-flex gap-2 mb-4">
                @if (Auth::user()->role=="admin")
                    <button type="button" class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#deleteModal">
                        <i class="fas fa-trash-alt"></i> حذف العضو
                    </button>
                @endif


            @if (Auth::user()->id==$User->id or Auth::user()->role == "admin" )
                <a href="/auth/users/{{$User->id}}/edit" class="btn btn-primary">
                    @if ($images[0])
                        <img src="{{ asset( $images[0]) }}" alt="لوحة التحكم" class="img-profile rounded-circle" width="30" height="30">
                    @endif

                    <i class="fas fa-arrow-left"></i> تعديل أو إضافة تفاصيل أخرى
                </a>
            @endif

        </div>
            <a href="{{ url()->previous() }}" class="btn btn-secondary">
                <i class="fas fa-arrow-left"></i> العودة للصفحة السابقة
            </a>


        @if (Auth::user()->role=="admin")
            <div class="modal fade" id="deleteModal" tabindex="-1" aria-labelledby="deleteModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered">
                        
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="deleteModalLabel"><i class="fas fa-exclamation-triangle text-danger"></i> تأكيد الحذف</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            هل أنت متأكد من أنك تريد حذف هذا العضو؟
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">إلغاء</button>
                            <form action="{{ route('auth.users.destroy', $User) }}" method="POST">
                                @csrf
                                @method('DELETE')
                                <button type="submit" class="btn btn-danger">
                                    <i class="fas fa-trash-alt"></i> نعم، احذف
                                </button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        @endif

    </article>
</x-layoutAdm>
