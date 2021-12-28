function ftable ( M, varargin)

%==========================================================================
% ftable( M, varargin)
%--------------------------------------------------------------------------
%
% Gibt textformatierte Tablelle mit Kopf-/Fußzeile/-spalte
% M ist Double Matrix or a table
%
% Optionen
% --------
%
% 'KopfZeile'
% 'Kopfspalte'
% 'Kommastellen'
% 'Ueberschrift'
% 'clc'
% 'Spaltenbreite'
% 'Fuszzeile'         Ein function handle, das für jede Spalte ausgeführt
%                     wird.
%
%============================================================== Grzegorz ==

% Defaults
fid = 1;
intMinColWidth = 6;
intKommastellen = 3;
logCLC = false;
% Defaults - ENDE

for kk=1:2:(nargin-1)
    if strcmpi('Ueberschrift', varargin{kk})
        strUeberschrift = varargin{kk+1};
        continue
    end
    if strcmpi('KopfZeile', varargin{kk})
        assert(iscell(varargin{kk+1}), ...
            'Kopfzeilen must be a cell array.') ;
        strKopfzeile = varargin{kk+1};
        continue
    end
    if strcmpi('Kopfspalte', varargin{kk})
        assert(iscell(varargin{kk+1}), ...
            'Kopfspaltenvektor must be a cell array.') ;
        strKopfspalte = varargin{kk+1};
        continue
    end
    if strcmpi('Kommastellen', varargin{kk})
        intKommastellen = varargin{kk+1};
        continue
    end
    if strcmpi('clc', varargin{kk})
        logCLC = varargin{kk+1};
        continue
    end
    if strcmpi('Spaltenbreite', varargin{kk})
        doMinColWidth = varargin{kk+1};
        continue
    end
    if strcmpi('FileID', varargin{kk})
        fid = varargin{kk+1};
        continue
    end
    if strcmpi('fuszzeile', varargin{kk})
        h_Fuszzeile = varargin{kk+1};
        assert(isa(h_Fuszzeile, 'function_handle'), ...
            'You must provide a function handle for the fuszzeile.')
        continue
    end
    error(['Argument ' varargin{kk} ' nicht gefunden.'])
end

% if istable(M)
%     if ~exist('strKopfspalte', 'var')
%        strKopfspalte = M.Properties.RowNames ;
%    end
%    if ~exist('strKopfzeile', 'var')
%        strKopfzeile = M.Properties.VariableNames ;
%    end
%    M = M.Variables ;
%end
% Dependencies
C = num2cell(M);
rowNum = size(M,1) ;
colNum = size(M, 2) ;
% Dependencies - ENDE

if logCLC
    clc
end
if exist('strUeberschrift', 'var')
    strUnderline = repmat('=', size(strUeberschrift)) ;
    fprintf(fid, '\n%s\n%s\n', strUeberschrift, strUnderline) ;
end
if ~exist('strKopfzeile', 'var') && ~exist('strKopfspalte', 'var')
    if ~exist('doMinColWidth', 'var')
        doMinColWidth = intMinColWidth;
    end
    
    charColumnFormat = [repmat(['%' num2str(doMinColWidth+2) '.' num2str(intKommastellen) 'f\t'], [1 size(M,2)]) '\n'];

    C = C';
    fprintf(fid, charColumnFormat, C{:});
end
if exist('strKopfzeile', 'var') && ~exist('strKopfspalte', 'var')
    if ~exist('doMinColWidth', 'var')
        doMinColWidth = max(size(char(strKopfzeile),2), intMinColWidth);
    end
    fprintf(fid, [repmat(['%' num2str(doMinColWidth+2) 's\t'], [1 size(M,2)]) '\n'], strKopfzeile{:});
    
    charColumnFormat = [repmat(['%' num2str(doMinColWidth+2) '.' num2str(intKommastellen) 'f\t'], [1 size(M,2)]) '\n'];

    C = C';
    fprintf(fid, charColumnFormat, C{:});
end
if exist('strKopfzeile', 'var') && exist('strKopfspalte', 'var') && length(strKopfspalte) == (size(M,1) + 1)
    if ~exist('doMinColWidth', 'var')
        doMinColWidth = max([size(char(strKopfzeile),2)  intMinColWidth  size(char(strKopfspalte),2)]);
    end
    fprintf(fid, [repmat(['%' num2str(doMinColWidth+2) 's\t'], [1 size(M,2)+1]) '\n'], strKopfspalte{1}, strKopfzeile{:});
    
    charColumnFormat = ['%' num2str(doMinColWidth+2) 's\t' repmat(['%' num2str(doMinColWidth+2) '.' num2str(intKommastellen) 'f\t'], [1 size(M,2)]) '\n'];
    
    C = [strKopfspalte(2:end)' C]';
    fprintf(fid, charColumnFormat, C{:});
end

if exist('strKopfzeile', 'var') && exist('strKopfspalte', 'var') && length(strKopfspalte) == size(M,1) 
    if ~exist('doMinColWidth', 'var')
        doMinColWidth = max([size(char(strKopfzeile),2)  intMinColWidth  size(char(strKopfspalte),2)]);
    end
    fprintf(fid, [repmat(['%' num2str(doMinColWidth+2) 's\t'], [1 size(M,2)+1]) '\n'], '', strKopfzeile{:});
    
    charColumnFormat = ['%' num2str(doMinColWidth+2) 's\t' repmat(['%' num2str(doMinColWidth+2) '.' num2str(intKommastellen) 'f\t'], [1 size(M,2)]) '\n'];
    
    C = [strKopfspalte(:) C]';
    fprintf(fid, charColumnFormat, C{:});
end

if ~exist('strKopfzeile', 'var') && exist('strKopfspalte', 'var') && length(strKopfspalte) == size(M,1) 
    if ~exist('doMinColWidth', 'var')
        doMinColWidth = max([intMinColWidth  size(char(strKopfspalte),2)]);
    end
    charColumnFormat = ['%' num2str(doMinColWidth+2) 's\t' repmat(['%' num2str(doMinColWidth+2) '.' num2str(intKommastellen) 'f\t'], [1 size(M,2)]) '\n'];
    
    C = [strKopfspalte(:) C]';
    fprintf(fid, charColumnFormat, C{:});
end

if exist('h_Fuszzeile', 'var') 
    c_fusz = cell(1, colNum) ;
    for kk = 1:colNum
        c_fusz{1, kk} = h_Fuszzeile(M(:,kk)) ;
    end
    if exist('strKopfspalte', 'var')
        fprintf(fid, '%s\n', repmat('-', [1 (1+colNum) * (doMinColWidth+intKommastellen+2) + 2]) );
        charColumnFormat = ['%' num2str(doMinColWidth+2) 's\t' repmat(['%' num2str(doMinColWidth+2) '.' num2str(intKommastellen) 'f\t'], [1 size(M,2)]) '\n'];
        fprintf(fid, charColumnFormat, '', c_fusz{:});
    else
        fprintf(fid, '%s\n', repmat('-', [1 colNum * (doMinColWidth+intKommastellen+2)]) );
        charColumnFormat = [repmat(['%' num2str(doMinColWidth+2) '.' num2str(intKommastellen) 'f\t'], [1 size(M,2)]) '\n'];
        fprintf(fid, charColumnFormat, c_fusz{:});
    end
    
end

