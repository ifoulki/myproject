<x-layoutAdm page='إدارة الاختبارات'>

        <article class="content">

            <h1 class="big-title" id="title"> لائحة الاختبارات </h1>

            @if ($exams->count())
                @foreach ($exams as $exam)
                    <div class="listes-contenu">

                        <div class="image-caption">
                            <a href="{{ route('exams.show', $exam) }}">
                                @php
                                    $images = explode(",", $exam->Myimage);
                                @endphp
                                <img src="{{ asset('images/exams/' . $images[0]) }}"
                                    alt="{{ $exam->title }}">
                            </a>
                        </div>
                        <div class="listes-contenu-art">
                            <a href="{{ route('exams.show', $exam) }}">
                                <div class="listes-title-contenu">
                                    <h2>{{ $exam->title }}</h2>
                                    <p style="color:black; text-align:justify">
                                        &emsp;{{ Str::limit($exam->Mydescription, 100, '...') }}
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
                                <form action="{{ route('exams.destroy', $exam) }}" method="POST" style="margin: 0;">
                                    @csrf
                                    @method('DELETE')
                                    <button class="btn btn-danger">
                                        <i class="fas fa-trash-alt"></i> 
                                        حدف الاختبار
                                    </button>
                                </form>

                                <a href="{{ route('exams.show', $exam) }}" class="btn btn-secondary">
                                    <i class="fas fa-book-open" ></i>
                                    معاينة الاختبار 
                                </a>

                                <a href="{{ route('exams.edit', $exam) }}" class="btn btn-primary">
                                    <i class="fas fa-edit"></i> تعديل الاختبار
                                </a>
                            </div>
                        </div>
                    </div>

                    <hr>
                @endforeach
                <div class="pagination-wrapper">
                    {{ $exams->links('vendor.pagination.bootstrap-5') }}
                </div>
            @else
                <p>لا توجد اختبارات حاليا !</p>
            @endif
        </article>
</x-layoutAdm>
