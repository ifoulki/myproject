<x-layoutAdm page='مراجعة الكتب'>

    <div class="content-grid content">
        <h1 style="margin-right: 25%"  class="big-title" id="title">مراجعة الكتب
            <br><i class="fas fa-book"></i></h1>

        @if ($books->count())
            @foreach ($books as $book)
                @php 
                    $direction = in_array("rtl", explode(',', $book->the_type)) ? "rtl" : "ltr"; 
                    $images = explode(",", $book->Myimage);
                    $isPublic = $book->visibility_status == 'public';
                @endphp

                <div class="book" dir="{{ $direction }}">
                    <a href="{{ route('books.show', $book) }}">
                        <figure>
                            <img src="{{ asset('images/books/' . $images[0]) }}" alt="{{ $book->title }}">
                            <figcaption class="edit-book-title book-title">{{ $book->title }}</figcaption>
                        </figure>
                        <hr>
                    </a>
                    <div class="listes-contenu-VD">
                        
                        <a title="تعديل الكتاب" href="{{ route('books.edit', $book) }}" class="btn btn-secondary">
                            <i class="fas fa-edit"></i>
                        </a>

                        <form action="{{ route('books.destroy', $book) }}" method="POST" style="display:inline;">
                            @csrf
                            @method('DELETE')
                            <button class="btn btn-danger" title="حدف الكتاب">
                                <i class="fas fa-trash-alt"></i>
                            </button>
                        </form>

                        <a title="معاينة الكتاب" href="{{ route('books.show', $book) }}" class="btn btn-primary" >
                            <i class="fas fa-book-open"></i>
                        </a>

                    </div>
                </div>
            @endforeach

            <div class="pagination-wrapper">
                {{ $books->links('vendor.pagination.bootstrap-5') }}
            </div>
        @else
            <p>لا توجد كتب متاحة</p>
        @endif
    </div>
</x-layoutAdm>