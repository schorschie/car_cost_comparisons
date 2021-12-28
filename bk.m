function [pM, pK, G] = bk(doAK, doVK, doST, doV, doSP,doRW,  doLL , doJ, varargin)


    % =====================================================================
    %  bk(doAK, doVK, doST, doV, doSP,doRW,  doLL , doJ, strE)
    % ---------------------------------------------------------------------
    % 
    %  doAK,    Anschaffungskosten, einmalig
    %  doVK,    Versicherungskosten, jaehrlich
    %  doST,    Steuern, jaehrlich
    %  doV,     Verbrauch in l/100km
    %  doSP,    Durschnittlicher Spritpreis ueber Haltedauer
    %  doRW,    Reparatur und Wartungskosten, jaehrlich
    %  doLL,    Jahreslaufleistung
    %  doJ,     Haltedauer in Jahren
    % 
    %  Optional
    %  --------
    %
    %  strE             Name der Kraftstoffeinheit, default: l
    %  Wertverlustplot  Monatlich Kosten mit Werverlust, default: false
    %  KreditHebelPlot  Break Even für Annuitätendarlehen, default: false
    %  tablePlot        Print table in console, default: true 
    %  label            Label für Betriebskosten, default: ''
    %  
    %  Examples
    %  --------
    %
    %    bk(43000, 1000, 0, 18, 0.29, 1000, 15000, 6, 'label', 'Model Y Std. inkl. Umweltbonus', 'stre', 'kWh')
    %
    %    bk(16903, 775, 230, 6.3, 1.16, 2000, 27000, 6.76, 'label', 'BMW 3er, Maximus')
    %
    % ========================================================= Grzegorz ==

    
    
if nargin < 8
    help bk
    return
end

strE = 'l';
loWVPlot = false ;
loKHPlot = false ;
% plotPie = false;
loTablePlot = true ;
strLabel = '';
for kk=1:2:length(varargin)
    if strcmpi('strE', varargin{kk})
        strE = varargin{kk+1} ;
        continue
    end
%     if strcmpi('Kuchen', varargin{kk})
%         plotPie = varargin{kk+1} ;
%         continue
%     end
    if strcmpi('Wertverlustplot', varargin{kk})
        loWVPlot = varargin{kk+1} ;
        continue
    end
    if strcmpi('KreditHebelPlot', varargin{kk})
        loKHPlot = varargin{kk+1} ;
        continue
    end
    if strcmpi('tablePlot', varargin{kk})
        loTablePlot = varargin{kk+1} ;
        continue
    end
    if strcmpi('label', varargin{kk})
        strLabel = varargin{kk+1} ;
        continue
    end
    error(['Parameter ' varargin{kk} ' not found.'])
end

doLL  = doLL * doJ ;
doGAn = [doAK                      doAK/doJ                       1/12* doAK/doJ                         doAK/doLL*100];
doGVK = [doVK*doJ                  doVK                           1/12* doVK                             doVK*doJ/doLL*100];
doGRW = [doRW*doJ                  doRW                           1/12* doRW                             doRW*doJ/doLL*100];
doGST = [doST*doJ                  doST                           1/12* doST                             doST*doJ/doLL*100];
doGSP = [doV * doSP * doLL / 100   doV * doSP * doLL / 100 / doJ  1/12* doV * doSP * doLL / 100 / doJ    doV * doSP  ];

G = [doGAn; doGVK; doGST; doGRW; doGSP];

if loWVPlot
%     try 
        close(findobj('Name', 'Verbrauchskosten'))
%     end
    x = (0:doJ) ;
    p = 1 ./ (x+0.48).^(0.23)  - 0.24 ;
    wv = -diff(p) * doAK ;
    WVpM = wv / 12;
    S = [WVpM; G(2:end,3) * ones(1,numel(WVpM)) ];
    if numel(WVpM) == 1
        S(1,2) = 0 ; % Workaround, pad a second row with zeros;
    end
    figure('Name', 'Verbrauchskosten')
    bar(S', 'stacked');
    legend({'Wertverlust', 'Versucherung', 'Wartung', 'Steuern', 'Kraftstoff'})
    xlabel('Haltejahr')
    ylabel('Monatliche Kosten')
%     title('Verbrauchskosten')
    grid on 
end

if loKHPlot
%     try
        close(findobj('Name', 'Kredithebel'))
%     end
    x = (0:doJ) ;
    p = (1 ./ (x+0.48).^(0.23)  - 0.24 ) * doAK ;
    k = [1.1 * doAK 0] ;
    figure('Name', 'Kredithebel')
    plot(x, p)
    hold on
    plot([0 doJ], k) ;
end
home
if loTablePlot
    
    fprintf(1, 'Betriebskosten'), fprintf(1, ' ( %s )\n', strLabel) ;
    fprintf(1, '=============='), fprintf(1, '%s\n\n', char(double('=') * (ones(1, numel(strLabel)+5)))) ;
    fprintf(1, 'Wertverlust, einmalig                                %s: %8.2f\n', repmat(' ', [1, numel(strE)-1]), doAK) ;
    fprintf(1, 'Versicherungskosten, jährlich                        %s: %8.2f\n', repmat(' ', [1, numel(strE)-1]), doVK) ;
    fprintf(1, 'Steuern, jährlich                                    %s: %8.2f\n', repmat(' ', [1, numel(strE)-1]), doST) ;
    fprintf(1, 'Verbrauch in %s/100 km                                : %8.2f\n', strE, doV ) ;
    fprintf(1, 'Durchschnittlicher Spritpreis über Haltedauer [/%s]  : %8.2f\n', strE, doSP) ;
    fprintf(1, 'Reparatur und Wartungskosten, jährlich               %s: %8.2f\n', repmat(' ', [1, numel(strE)-1]), doRW) ;
    fprintf(1, 'Jahreslaufleistung [tkm]                             %s: %8d\n', repmat(' ', [1, numel(strE)-1]), doLL / doJ) ;
    fprintf(1, 'Gesamtlaufleistung [tkm]                             %s: %8d\n', repmat(' ', [1, numel(strE)-1]), doLL) ;
    fprintf(1, 'Haltedauer in Jahren                                 %s: %8.2f\n\n', repmat(' ', [1, numel(strE)-1]), doJ) ;
    
    ftable(G, 'KopfZeile',  {'Gesamt', 'Jährlich', 'Monatlich', 'pro KM'}, ...
        'Kopfspalte', {'Wertverlust', 'Versicherung',  'Steuern', 'Reparaturen', 'Verbrauch'}, ...
        'kommastellen', 2, ...
        'fuszzeile', @(x)sum(x)) ;

%     if plotPie
%         BK.plotPie();
%     end
end
if nargout >= 1
    pM = doGAn(3)+ doGVK(3) + doGRW(3) + doGST(3) + doGSP(3);
end
if nargout >= 2
    pK = (doGAn(4)+ doGVK(4) + doGRW(4) + doGST(4) + doGSP(4)) / 100;
end

