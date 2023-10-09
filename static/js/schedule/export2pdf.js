const convertToPDF = (element_id, str='') => {
    console.log(str);
    console.log(element_id);
    const pdf = jspdf.jsPDF();
    const bootstrapStyles = '<link rel="stylesheet" href="/static/bootstrap_v5.1.3/bootstrap.min.css"';
        //const bootstrapStyles = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css"';
        pdf.html(bootstrapStyles, { x: 10, y: 10 });
        const element = document.getElementById(element_id);
        console.log(element);
        const filename = str.replace('Расписание на ', '') + '.pdf';
        html2canvas(element).then(canvas => {
            const imageData = canvas.toDataURL('image/png');
            console.log(imageData);
            pdf.addImage(imageData, 'PNG', 10, 5, 180, 0);
            pdf.save(filename);
          });

 }