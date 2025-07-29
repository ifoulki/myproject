<x-layoutAdm page='دروس'>

        <article class="content">

            <h1 class="big-title" id="title">لائحة الدروس </h1>

            @if ($cours->count())
                @foreach ($cours as $cour)
                    <div class="listes-contenu">

                        <div class="image-caption">
                            <a href="{{ route('cours.show', $cour) }}">
                                @php
                                    $images = explode(",", $cour->Myimage);
                                @endphp
                                <img src="{{ asset('images/cours/' . $images[0]) }}"
                                    alt="{{ $cour->title }}">
                            </a>
                        </div>
                        <div class="listes-contenu-art">
                            <a href="{{ route('cours.show', $cour) }}">
                                <div class="listes-title-contenu">
                                    <h2>{{ $cour->title }}</h2>
                                    <p style="color:black; text-align:justify">
                                        &emsp;{{ Str::limit($cour->Mydescription, 100, '...') }}
                                        <span
                                            style="color: #9d6e25;
                                                        justify-content: center;
                                                        font-family: Tahoma;">
                                            إقرأ المزيد
                                        </span>
                                    </p>
                                </div>
                            </a>
                            <div style="display: flex; gap: 15px; align-items: center;">
                                <form action="{{ route('cours.destroy', $cour) }}" method="POST" style="margin: 0;">
                                    @csrf
                                    @method('DELETE')
                                    <button class="btn btn-danger">
                                        <i class="fas fa-trash-alt"></i> 
                                        حدف الدرس
                                    </button>
                                </form> 

                                <a href="{{ route('cours.show', $cour) }}" class="btn btn-secondary">
                                    <i class="fas fa-book-open" ></i>
                                    مراجعة الدرس
                                </a>

                                <form action="{{ route('cours.update', $cour) }}" method="POST" style="margin: 0;">
                                    @csrf
                                    @method('PATCH')
                                    
                                    <button title="{{ $cour->visibility_status == 'public' ? 'أنقر لجعله يظهر للمدراء فقط' : 'أنقر لجعله يظهر للجميع ' }}" class="btn {{ $cour->visibility_status == 'public' ?  'btn-success':'btn-warning'  }}" type="submit" name="visibility" value="{{ $cour->visibility_status == 'public' ? 'restricted' : 'public' }}">
                                        <i class="fas {{ $cour->visibility_status == 'public' ?  'fa-eye':'fa-eye-slash'  }}"></i>
                                        {{ $cour->visibility_status == 'public' ? 'الدرس يظهر للجميع' : 'الدرس يظهر للمدراء فقط ' }}
                                    </button>
                                </form>

                                <a href="{{ route('cours.edit', $cour) }}" class="btn btn-primary">
                                    <i class="fas fa-edit"></i> تعديل الدرس
                                </a>
                            </div>
                        </div>
                    </div>

                    <hr>
                @endforeach
                <div class="pagination-wrapper">
                    {{ $cours->links('vendor.pagination.bootstrap-5') }}
                </div>
            @else
                <p>لا توجد دروس حاليا !</p>
            @endif
        </article>
</x-layoutAdm>
