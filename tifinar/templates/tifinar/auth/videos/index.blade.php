<x-layoutAdm page='الفيديوهات'>
    <div class="content-grid content">
        <h1 style="margin-right: 25%" class="big-title" id="title">مراجعة الفيديوهات
            <br><i class="fas fa-video"></i></h1>

        @if ($videos->count())
            @foreach ($videos as $video)
            @php
                $images = explode(",", $video->Myimage);
            @endphp

                <div  class="video" dir="{{ $video->dir }}">
                    <a href="{{ route('auth.videos.show', $video) }}">
                        <figure>
                            <img src="{{ asset('images/videos/' . $images[0]) }}" alt="{{ $video->title }}">
                            <figcaption class="edit-video-title">{{ $video->title }}</figcaption>
                        </figure>

                        <hr>
                    </a>
                    <div class="listes-contenu-VD">
                        <a title="مشاهدة الفيديو" href="{{ route('auth.videos.edit', $video) }}" class="btn btn-primary">
                            <i class="fas fa-play-circle"></i>
                        </a>

                        <form action="{{ route('auth.videos.destroy', $video) }}" method="POST" style="display:inline;">
                            @csrf
                            @method('DELETE')
                            <button class="btn btn-danger" title="حدف الفيديو">
                                <i class="fas fa-trash-alt"></i>
                            </button>
                        </form>

                        <a title="تعديل الفيديو" href="{{ route('auth.videos.edit', $video) }}" class="btn btn-secondary">
                            <i class="fas fa-edit"></i>
                        </a>

                        <hr>
                    </div>
                </div>
            @endforeach

            <div class="pagination-wrapper">
                {{ $videos->links('vendor.pagination.bootstrap-5') }}
            </div>
        @else
            <p>لا توجد فيديوهات متاحة</p>
        @endif
    </div>
</x-layoutAdm>