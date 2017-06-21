The file `style.py` provides a decorator to make figures suited for publication in A&A articles.

Intended use is:

    from styler import styler
    from styler import colors, colors_named

    @styler
    def f(fig, *args, **kwargs):
        ax = fig.add_subplot(111)
        
        ax.plot([0,1,2,3], [30, 35, 40, 45], '-o', color=colors_named['green'])
        
        ax.set_xlabel('X axis')
    
    f(type='A&A', save='output_figure.pdf', tight=True)

