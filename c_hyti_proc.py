# vital imports
import matplotlib.pyplot as plt
import numpy as np

class c_hyti_proc :
    nsamps= 324
    nlines= 256
    
    def __init__(self, ns, nl) :
        self.nsamps = ns 
        self.nlines = nl
        self.nbands = 100
        self.nsamps_seg = 200
        self.nsamps_seg2 = self.nsamps_seg*2
        
        
    def extract_flatten (self, fname):
        tmparr = np.fromfile(fname, dtype=np.uint16).reshape((self.nbands, self.nlines, self.nsamps))
        flatten = np.mean(tmparr, axis=0)
        return flatten
    
    # create one more fcn to extract from the big array at the correct starting point
    def extract(self,bigarr,zmfac,startloc,npts):
        startind = int(zmfac*startloc)
        endind = int((startind+self.nsamps_seg)*zmfac)
        outarr=bigarr[startind:endind:zmfac]
        return outarr
    
    def sp_interpolate(self, inarr, zoomfac):
        npts=inarr.shape[0]
        npts2=int(npts/2)

        nptsbig=npts*zoomfac
        # first fft the inarr
        bigarr=np.zeros(npts*zoomfac,dtype=np.complex64)
        fft_inarr=np.fft.fft(inarr)
        bigarr[0:npts2]=fft_inarr[0:npts2]
        bigarr[nptsbig-npts2:]=fft_inarr[npts2:]
        ifftarr=np.abs(np.fft.ifft(bigarr))
        return (ifftarr)
    
    # given a profile segment, do the "tircis" style processing
    def proc_tircis(self, in_profile, starts):
        x400 = np.arange(self.nsamps_seg2)
        # extract
        bb_seg = in_profile[starts:starts+self.nsamps_seg]
        # mirror
        bb_mirror= np.append(bb_seg[::-1],bb_seg)
        #plt.plot(bb90_mirror)
        # fit a 2d polynomial to this fcn and subtract it 
        pfit=np.polyfit(x400,bb_mirror,2)
        yfit=np.polyval(pfit,x400)
        # plt.plot(yfit)
        # plt.show()
        # then subtract the polynomial fcn(yfit) from the mirrored array
        bb_zmean=bb_mirror-yfit
        # plt.plot(bb90_zmean)
        # plt.show()
        # apod400 is the triangular apodizing fcn
        apodtmp=np.linspace(0,1,self.nsamps_seg)
        apod400=np.append(apodtmp,apodtmp[::-1])

        # then multiply the zmean fcn by the apod
        bb_interf=bb_zmean*apod400
        bb_fft=np.fft.fft(bb_interf)
        return(np.abs(bb_fft))

