<x-layoutAdm 
    page='الإدارة'
    description='إنضم إلى عائلة تيفيناغ.كوم وساهم في الرقي بالمحتوى العربي في الأنترنيت بنشر مساهمتك في مجلتنا سواء كانت مقالات أو أخبار أو دروس ... إلخ، موقعنا يضم أيضا مكتبة كبيرة تحتوي على كتب متنوعة ومجالات وحتى مطبوعات مدرسية ونماذج اختبارات، نحن نرحب بأي مساهمة يمكن أن تفيد زوارنا'
>
    <section class="content">

            <h2 class="mt-5">لوحة تحكم الزوار</h2>

            <div class="row">
                <div class="col-12 col-md-6 mt-4">
                    <h4>إحصائيات الزيارات حسب عنوان IP</h4>
                    <div class="form">
                        <h4>عدد الزيارات لكل IP</h4>
                        <canvas id="ipVisitsChart" style="width: 100%; height: 400px;"></canvas>
                    </div>
                </div>

                <div class="col-12 col-md-6 mt-4">
                    <h4>عدد الزيارات حسب نوع الجهاز</h4>
                    <div class="form">
                        <canvas id="deviceVisitsChart" style="width: 100%; height: 400px;"></canvas>
                    </div>
                </div>
            </div>

            <div class="row mt-4">
                <div class="col-12 col-md-6">
                    <h4>عدد الزيارات لكل صفحة</h4>
                    <div class="form">
                        <canvas id="pageVisitsChart" style="width: 100%; height: 400px;"></canvas>
                    </div>
                </div>

                <div class="col-12 col-md-6">
                    <h4>عدد الزيارات حسب التاريخ (آخر 7 أيام)</h4>
                    <div class="form">
                        <canvas id="dailyVisitsChart" style="width: 100%; height: 400px;"></canvas>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <script>
        const ipVisitsData = {
            labels: [
                @foreach($ipVisits->keys() as $ip)
                    '{{ $ip }}',
                @endforeach
            ],
            datasets: [{
                label: 'عدد الزيارات',
                data: [
                    @foreach($ipVisits->values() as $visits)
                        {{ $visits }},
                    @endforeach
                ],
                backgroundColor: 'rgba(153, 102, 255, 0.6)',
                borderColor: 'rgba(153, 102, 255, 1)',
                borderWidth: 1
            }]
        };

        const ipVisitsChart = new Chart(document.getElementById('ipVisitsChart'), {
            type: 'bar',
            data: ipVisitsData,
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            font: { size: 14 }
                        }
                    },
                    x: {
                        ticks: {
                            font: { size: 14 }
                        }
                    }
                },
                plugins: {
                    legend: {
                        labels: { font: { size: 16 } }
                    }
                }
            }
        });

        const pageVisitsData = {
            labels: [
                @foreach($pageVisits->keys() as $key)
                    '{{ $key }}',
                @endforeach
            ],
            datasets: [{
                label: 'عدد الزيارات',
                data: [
                    @foreach($pageVisits->values() as $value)
                        {{ $value }},
                    @endforeach
                ],
                backgroundColor: 'rgba(54, 162, 235, 0.6)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        };

        const deviceVisitsData = {
            labels: [
                @foreach($deviceVisits->keys() as $key)
                    '{{ $key }}',
                @endforeach
            ],
            datasets: [{
                label: 'عدد الزيارات',
                data: [
                    @foreach($deviceVisits->values() as $value)
                        {{ $value }},
                    @endforeach
                ],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.6)',
                    'rgba(54, 162, 235, 0.6)',
                    'rgba(255, 206, 86, 0.6)',
                    'rgba(75, 192, 192, 0.6)',
                    'rgba(153, 102, 255, 0.6)',
                    'rgba(255, 159, 64, 0.6)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        };

        const dailyVisitsData = {
            labels: [
                @foreach($dailyVisits->keys() as $date)
                    '{{ $date }}',
                @endforeach
            ],
            datasets: [{
                label: 'عدد الزيارات',
                data: [
                    @foreach($dailyVisits->values() as $value)
                        {{ $value }},
                    @endforeach
                ],
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        };

        const pageVisitsChart = new Chart(document.getElementById('pageVisitsChart'), {
            type: 'bar',
            data: pageVisitsData,
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { font: { size: 16 } }
                    },
                    x: {
                        ticks: { font: { size: 16 } }
                    }
                },
                plugins: {
                    legend: {
                        labels: { font: { size: 18 } }
                    }
                }
            }
        });

        const deviceVisitsChart = new Chart(document.getElementById('deviceVisitsChart'), {
            type: 'pie',
            data: deviceVisitsData,
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        labels: { font: { size: 18 } }
                    }
                }
            }
        });

        const dailyVisitsChart = new Chart(document.getElementById('dailyVisitsChart'), {
            type: 'line',
            data: dailyVisitsData,
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { font: { size: 16 } }
                    },
                    x: {
                        ticks: { font: { size: 16 } }
                    }
                },
                plugins: {
                    legend: {
                        labels: { font: { size: 18 } }
                    }
                }
            }
        });
    </script>
</x-layoutAdm>