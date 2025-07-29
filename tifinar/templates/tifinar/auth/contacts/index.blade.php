<x-layoutAdm page="لائحة الأعضاء">

    <article class="content">
        <h1>لائحة الأعضاء</h1>

        <div class="filter mt-4 p-4 border rounded shadow-sm bg-light">
            <form method="GET" action="{{ route('contacts.index') }}" class="d-flex flex-column flex-md-row align-items-md-center mb-3">
                <div class="input-group border rounded flex-grow-1 d-flex">
                    <input type="text" class="form-control search-input border-0 flex-grow-1" id="search" name="search" placeholder="ابحث عن عضو" value="{{ request('search') }}">
                    <button type="submit" class="btn btn-outline-primary search-btn flex-shrink-0" style="width: 50px;">
                        <i class="bi bi-search"></i>
                    </button>
                </div>
            </form>

        @if (Auth::user()->role == 'admin')
            <div class="vertical-line mx-3"></div>

            <form method="GET" action="{{ route('contacts.index') }}" class="d-flex flex-column flex-md-row align-items-md-center">
                <div class="input-group border rounded flex-grow-1 d-flex">
                    <select class="form-select border-0 flex-grow-1" name="the_type" id="the_type" aria-label="Select Category">
                        <option value="" disabled selected>اختر النوع</option>
                        <option value="Code" {{ request('the_type') == 'Code' ? 'selected' : '' }}>كلمة سرية</option>
                        <option value="collegue" {{ request('the_type') == 'collegue' ? 'selected' : '' }}>زملاء العمل</option>
                        <option value="PDG" {{ request('the_type') == 'PDG' ? 'selected' : '' }}>أصحاب الشركات</option>
                        <option value="Sup" {{ request('the_type') == 'Sup' ? 'selected' : '' }}>رؤساء العمل</option>
                        <option value="Famille" {{ request('the_type') == 'Famille' ? 'selected' : '' }}>العائلة</option>
                        <option value="Connaissances" {{ request('the_type') == 'Connaissances' ? 'selected' : '' }}>المعارف</option>
                        <option value="Num.Pro" {{ request('the_type') == 'Num.Pro' ? 'selected' : '' }}>أرقام مهنية</option>
                        <option value="Ami (e)" {{ request('the_type') == 'Ami (e)' ? 'selected' : '' }}>الأصدقاء</option>
                        <option value="default" {{ request('the_type') == 'default' ? 'selected' : '' }}>غير معروف</option>
                    </select>
            
                    <button type="submit" class="btn btn-outline-success search-btn flex-shrink-0" aria-label="Filter" style="width: 50px;">
                        <i class="bi bi-search"></i>
                    </button>
                </div>
            </form>
        @endif
            
        </div>

        @if ($contacts->isEmpty())
            <p>لا توجد بيانات للعرض.</p>
        @else
            <div class="container mt-5">
                <div class="text-left mb-4">
                    <a title="إضافة عضو جديد" href="{{ route('contacts.create') }}" class="btn btn-primary btn-sm">
                        <i class="fas fa-user-plus"></i> إضافة عضو جديد
                    </a>
                </div>

                <div class="table-responsive">
                    <table class="table table-bordered table-hover">
                        <thead class="thead-dark">
                            <tr>
                                <th class="img-contacnt">ID</th>
                                <th class="img-contacnt">الصورة</th>
                                <th>الاسم</th>
                                <th>Tel</th>
                                <th>التحكم</th>
                            </tr>
                        </thead>
                        <tbody>
                            @foreach ($contacts as $contact)
                                @php
                                    $images = explode(',', $contact->path);
                                    shuffle($images);
                                    if (count($images) > 0 && !empty($images[0] )) {
                                        $src = asset('images/contacts/' . $images[0]);
                                    } else {
                                        $src = $contact->gender == 'Female' ? asset('assets/female.webp') : asset('assets/male.webp');
                                    }
                                @endphp
                                <tr>
                                    <td><a href="{{ route('contacts.show', $contact) }}">{{ $contact->contacts_id }}</a></td>
                                    <td class="img-contacnt">
                                        <a href="{{ $src }}" data-lightbox="gallery" data-title="{{ $contact->Prenom }} {{ $contact->Nom }}">
                                            <img src="{{ $src }}" alt="{{ $contact->Prenom }} {{ $contact->Nom }}" class="img-thumbnail" style="width: 80px; height: 80px;">
                                        </a>
                                    </td>
                                    <td>
                                        <a href="{{ route('contacts.show', $contact) }}">
                                            {{ $contact->Prenom }} {{ $contact->Nom }}
                                        </a>
                                    </td>
                                    <td>
                                        <a href="{{ route('contacts.show', $contact) }}">
                                            {{ $contact->Tel }}
                                        </a>
                                    </td>
                                    <td>
                                        <a title="تعديل معلومات العضو" href="{{ route('contacts.edit', $contact) }}" class="btn btn-warning btn-sm"><i class="fas fa-edit"></i></a>
                                        <form action="{{ route('contacts.removeUserIdFromAuthor', $contact->contacts_id) }}" method="POST">
                                            @csrf
                                            <button title="حذف العضو" type="submit" class="btn btn-danger btn-sm" onclick="return confirm('هل أنت متأكد من حذف هذا العضو؟');"><i class="fas fa-trash-alt"></i></button>
                                        </form>
                                    </td>
                                </tr>
                            @endforeach
                        </tbody>
                    </table>
                    
                </div>
            </div>
        @endif

        <div class="pagination-wrapper">
            {{ $contacts->appends(request()->input())->links('vendor.pagination.bootstrap-5') }}
        </div>
    </article>

<script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.6/dist/umd/popper.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/lightbox2/dist/js/lightbox-plus-jquery.js"></script>
</x-layoutAdm>
