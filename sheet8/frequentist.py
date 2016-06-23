#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ROOT import TMath, TF1


def probability(n, s, b):
    '''
    Returns the probability to observe n events if you expect s signal events
    and b background events
    Equivalent to: exp(-s-b)*(s+b)**n/TMath::Factorial(n)
    '''
    return TMath.PoissonI(n, s + b)

def pvalue_function_classical(x, par):
    '''
    If you expect s signal events and b background events, return the
    probability to observe more than n events: used for classical upper-limits
    on the total number of events (signal + background): CL_SB
    '''
    s = x[0]
    n = par[0]
    b = par[1]

    pvalue_sum = 0.
    for i in range(int(round(n)+1)):
      pvalue_sum += probability(i, s, b)

    if (s + b < 0):
        pvalue_sum = 1.  # s+b should be positive

    return pvalue_sum

def pvalue_function_cls(x, par):
    '''
    If you expect s signal events and b background events, return the
    probability to observe more than n events: used for normalized upper-limits
    on the total number of signal events: CL_S = CL_SB / CL_B
    '''

    s = x[0]
    n = par[0]
    b = par[1]

    pvalue_sum = 0.
    for i in range(int(round(n)+1)):
        pvalue_sum += probability(i, s, b)

    if (s + b < 0):
        pvalue_sum = 1. # s+b should be positive

    pvalue_sum2 = 0.    # probability to observe n or less events if no signal is expected
    for i in range(int(round(n)+1)):
        pvalue_sum2 += probability(i, 0, b)

    result = pvalue_sum / pvalue_sum2

    return result

def limit(n, b, pvalue, func):
    '''
    Compute the value of s for which you reach the given p-value, if you
    observe n events and expect b background events
    '''

    min = -1        # almost -infinity, since negetive values are not meaningful
    max = +10*(n+1) # almost +infinity on relevant scale

    # function of one parameter varying between min and max
    pvf = TF1("pvf", func, min, max, 2)

    pvf.SetParameter(0, n)
    pvf.SetParameter(1, b)

    limit = 0
    limit = pvf.GetX(pvalue, min, max)

    return limit
