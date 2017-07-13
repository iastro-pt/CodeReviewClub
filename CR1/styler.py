# matplotlib parameters for publication plots
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import re
import os

this_folder = os.path.dirname(__file__)


#### styler also provides colors for consistency
colors = ['#4878cf', '#6acc65', '#d65f5f', '#b47cc7', '#c4ad66', '#77bedb']
colors_named = {'blue': '#4878cf', 
                'green': '#6acc65',
                'red': '#d65f5f',
                'purple': '#b47cc7',
                'yellow': '#c4ad66',
                'lightblue': '#77bedb'
                }


params = {'text.latex.preamble': [r'\usepackage{lmodern}',
                                  r'\usepackage{amsfonts,amsmath,amssymb}',
                                  r'\mathchardef\mhyphen="2D',
                                  r'\DeclareMathOperator{\ms}{m\!\cdot\!s^{-1}}',
                                  r'\DeclareMathOperator{\kms}{km\!\cdot\!s^{-1}}'],
          'text.usetex' : True,
          'font.size'   : 8,
          'font.family' : 'lmodern',
          'text.latex.unicode': True,
          'axes.unicode_minus': True,
          }

class MyFormatter(ticker.ScalarFormatter):
  """ Axis ticks formatter to replace the big minus sign with a smaller, prettier one. """
  def __call__(self, x, pos=None):
    # call the original ScalarFormatter
    rv = ticker.ScalarFormatter.__call__(self, x, pos)
    # check if we really use TeX
    if plt.rcParams["text.usetex"]:
      # if we have the string ^{- there is a negative exponent
      # where the minus sign is replaced by the short hyphen
      rv = re.sub(r'-', r'\mhyphen', rv)

    if rv.endswith('.0'):
      rv = rv.replace('.0', '')

    return rv



### for the A&A article class
AandA_width = 3.543311946  # in inches = \hsize = 256.0748pt
AandA_full_width = 7.2712643025 # in inches = \hsize = 523.53 pt


default_figwidth = AandA_width
default_figheight_factor = 0.75

def styler(func):
  """
  This decorator provides a matplotlib figure with the right size
  and deals with its axes to make them suitable to plot in an A&A article.

  To be used as 

  @styler
  def f(fig, *args, **kwargs):
    # make the plot in figure `fig`

  f()

  
  Keyword arguments (to pass to the decorated function, f() above):
    type (str): One of 'A&A' or 'A&Afw' for one-column and two-column figures respectively
    save (str): The name of the file to save the figure, with extension (e.g. '.pdf' or '.png')

    dpi (int): The dots-per-inch of the figure, default 100
    axislw (float): Make the axes lines thicker or thiner, default 1
    tight (bool): Whether to call tight_layout on the figure

    formataxis (bool): Use a custom formatter for the axes tick labels
    formaty (bool): Apply custom formatter to y-axis
    formatx (bool): Apply custom formatter to x-axis

    verbose (bool): Print all supplied arguments
  """

  def inner(*args, **kwargs):

    ## print the arguments, for debugging
    if kwargs.get('verbose', False):
      from pprint import pprint
      print("Arguments were:")
      print(args)
      print(pprint(kwargs))


    figwidth, figheight = kwargs.get('figsize', (default_figwidth, default_figheight_factor))

    if figwidth is None: # the user can choose to only set figheight
      figwidth = default_figwidth
      # width_multiplier = 1.
    # else:
      # width_multiplier = figwidth

    # type of figure, can be 'a&a', 'a&afw'
    # by default, the lengths of 'a&a' are used
    figtype = kwargs.get('type', 'A&A')
    if figtype.lower() in ('a&a', 'onecolumn', 'one'): 
      figwidth = AandA_width
    if figtype.lower() in ('a&afw', 'twocolumns', 'two', 'full'): 
      figwidth = AandA_full_width

    # figwidth *= width_multiplier
    figheight = figheight * figwidth


    with plt.rc_context(params):
      # this creates the figure with the correct size
      dpi = kwargs.get('dpi', 100)
      fig = plt.figure(figsize=(figwidth, figheight), dpi=dpi)

      # now call the user function (the function they decoreated)
      func(fig, *args, **kwargs)

      # optionally make every line a bit wider
      axislw = kwargs.get('axislw', 1.)
      for ax in fig.axes:
        for axis in ['top','bottom','left','right']:
          ax.spines[axis].set_linewidth(axislw)
          xticks = ax.xaxis.get_ticklines()
          plt.setp(xticks, linewidth=axislw/2.)
          yticks = ax.yaxis.get_ticklines()
          plt.setp(yticks, linewidth=axislw/2.)

      # tight_layout ?
      tight = kwargs.get('tight', True)
      tightpad = kwargs.get('tightpad', 0.4)
      if tight:
        fig.tight_layout(pad=tightpad)

      # set the right formatter for the axis ticks and remove annoying offsets
      format_axis = kwargs.get('formataxis', True)
      format_yaxis = kwargs.get('formaty', True)
      format_xaxis = kwargs.get('formatx', True)
      ## attention: this next option assumes the user has set
      ## .is_colorbar attribute to the axis which contains the colorbar
      ## otherwise it will not work
      format_cbar = kwargs.get('formatcbar', True)
      if format_axis:
        if format_yaxis:
          for ax in fig.axes:
            try:
              ax.yaxis.get_major_formatter().set_useOffset(False)
              ax.xaxis.get_major_formatter().set_useOffset(False)
            except AttributeError:
              print('Cannot remove offset from axis, maybe using log axis?')

            try:
              if ax.is_colorbar and format_cbar:
                ax.yaxis.set_major_formatter(MyFormatter())
                ax.yaxis.get_major_formatter().set_useOffset(False)    
            except AttributeError:
              ax.yaxis.set_major_formatter(MyFormatter())
              ax.yaxis.get_major_formatter().set_useOffset(False)
        if format_xaxis:
          for ax in fig.axes:
            ax.xaxis.set_major_formatter(MyFormatter())
            ax.xaxis.get_major_formatter().set_useOffset(False)
        
      save = kwargs.get('save')
      if save is None:
        fig.show()
      else:
        assert type(save) in (str, str)
        fig.savefig(save, dpi=fig.dpi)

  return inner



if __name__ == '__main__':

  @styler
  def f(fig, *args, **kwargs):
    """ This function can use the `matplotlib.figure.Figure` in fig. """
    ax = fig.add_subplot(111)
    ax.plot([1,2,3])
    ax.set_xlabel(r'margin fig [s$^{-1}$]')
    ax.set_ylabel('y label [m]')


  @styler
  def g(fig, *args, **kwargs):
    from numpy import linspace, sin
    ax = fig.add_subplot(111)
    ax.plot(linspace(0,10), sin(linspace(0,10)))
    ax.set_xlabel(r'full width fig [s$^{-1}$]')
    ax.set_ylabel(r'sine [M$_\oplus$]')

  # call the function without arguments, `styler` will take care of
  # supplying it with the fig object
  # f(verbose=True)

  # test creating a column figure
  f(type='A&A', save='test_column_fig.pdf', tight=True)

  # test creating a full width figure
  g(type='A&AFW', figsize=(None, 0.4),
    save='test_fullwidth_fig.pdf', tight=True,
    axislw=0.4)

  ## make empty figures the right size
  @styler
  def empty(fig, *args, **kwargs):
    ax = fig.add_subplot(111)
    ax.text(0.31, 0.5, 'I am empty')

  empty(type='one', save='empty_onecolumn_fig.pdf', tight=True)
  empty(type='two', save='empty_twocolumn_fig.pdf', tight=True)
