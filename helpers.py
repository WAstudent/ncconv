import tempfile
import re
import copy
import pdb


def get_temp_path(suffix=''):
    """Return absolute path to a temporary file."""
    f = tempfile.NamedTemporaryFile(suffix=suffix)
    f.close()
    return f.name

def parse_polygon_wkt(txt):
    """Parse URL polygon text into WKT"""
    
    ## POLYGON ((30 10, 10 20, 20 40, 40 40, 30 10))
    ## POLYGON((30+10,10+20,20+40,40+40))
    
    txt = txt.lower()
    txt = txt.replace('+',' ')
    
    coords = re.match('.*\(\((.*)\)\)',txt).group(1)
    coords = coords.split(',')
    ## replicate last coordinate if it is not passed
    if coords[0] != coords[-1]:
        coords.append(coords[0])
    coords = ', '.join(coords)
    
    wkt = 'POLYGON (({0}))'.format(str(coords))
        
    return(wkt)

def merge_dict(*args):
    """
    Merge two dictionaries with dict values as lists.
    
    >>> one = dict(a=[1,2,3],b=['one'])
    >>> two = dict(a=[4,5,6],b=['two'])
    >>> three = dict(a=[7,8,9],b=['three'])
    >>> merge_dict(one,two,three)
    {'a': [1, 2, 3, 4, 5, 6, 7, 8, 9], 'b': ['one', 'two', 'three']}
    """
    
    def _gen():
        for ii in xrange(len(args)):
            try:
                yield(args[ii+1])
            except IndexError:
                raise StopIteration
    
    ## get the base dictionary
    b = copy.copy(args[0])
    ## loop through merging
    for t in _gen():
        for key,value in t.iteritems():
            b[key] += value
    return(b)

def html_table(ld,order):
    """
    Generate an HTML table code from a nested dictionary. DOEST NOT generate
    the <table> tag to allow table customization.
    
    >>> ld = [dict(month='January',savings='$100'),dict(month='April',savings ='$50')]
    >>> order = (('month','Month'),('savings','Savings'))
    >>> html_table(ld,order)
    """
    
    ## contains the formated html code
    dump = []
    
    tr = '<tr>{0}</tr>'
    th = '<th>{0}</th>'
    td = '<td>{0}</td>'
    
    ## set the headings
    dump.append(tr.format(''.join([th.format(o[1]) for o in order])))
    ## add the data
    for l in ld:
        dump.append(tr.format(''.join([td.format(l[o[0]]) for o in order])))
    
    return(''.join(dump))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    